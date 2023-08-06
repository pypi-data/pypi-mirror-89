import typing as t

import spacy
from spacy_langdetect import LanguageDetector

from bavard.common.serialization import Persistent
from bavard.common.pydantics import Tag
from bavard.dialogue_policy.data.conversations.actions import Actor
from bavard.dialogue_policy.models.classifier import Classifier
from bavard.dialogue_policy.data.conversations.conversation import Conversation
from bavard.mlops.web_service import WebService, endpoint
from bavard.mlops.pydantics import ChatbotPipelinePredictions, ChatbotPipelinePrediction, ChatbotPipelineInputs
from bavard.nlu.model import NLUModel


class ChatbotPipeline(WebService, Persistent):
    """
    A machine learning pipeline for chatbots that handles NLU parsing
    and dialogue policy prediction.
    """

    def __init__(self, config: dict = None):
        if config is None:
            config = {}
        self._fitted = False
        self._do_dp = False
        self._nlu_model = NLUModel(**config.get("nlu", {}))
        self._dp_model = Classifier(**config.get("dp", {}))
        self._use_ner_presets: bool = config.get('use_ner_presets', True)

        # TODO: Load spaCy models for multiple languages. Then detect the language at prediction time and apply
        #       the appropriate model.
        self.spacy_en = spacy.load('en_core_web_sm')
        self.spacy_en.add_pipe(LanguageDetector(), name='language_detector', last=True)

    def fit(self, agent: dict):
        self._nlu_model.train(agent["nluData"])
        if len(agent["trainingConversations"]) > 0:
            self._dp_model.fit(agent)
            self._do_dp = True
        else:
            self._do_dp = False
        self._fitted = True

    @endpoint(methods=["POST"])
    def predict(self, inputs: ChatbotPipelineInputs) -> ChatbotPipelinePredictions:
        """
        Takes `instances` (a list of conversations) and parses the intent of the final user
        utterance on each of them. Also, predicts the next agent action to take for
        each one. If the agent the pipeline was trained on had no training conversations, the pipeline will
        not use a dialogue policy model and its dialogue policy prediction will be `None`. If the final turn
        in any of the conversations is not a user turn and doesn't have an utterance, no NLU prediction will
        be made for that conversation and its NLU prediction will be `None`.
        """
        assert self._fitted
        convs = inputs.instances

        predictions = [ChatbotPipelinePrediction(nlu=None, dp=None)] * len(convs)

        # Parse the user utterances.
        utterances = [conv.get_final_user_utterance() for conv in convs]
        nlu_preds = self._nlu_model.predict(utterances).predictions
        for conv, utterance, pred, nlu_pred in zip(convs, utterances, predictions, nlu_preds):
            # If there is no utterance then the prediction for it won't make sense.
            if utterance:

                # Supplement NLU prediction with spaCy NER.
                if self._use_ner_presets:
                    conv_language = self._detect_conv_language(conv)
                    # TODO: Handle more languages.
                    if conv_language == 'en':
                        tags = nlu_pred.tags
                        doc = self.spacy_en(utterance)
                        for entity in doc.ents:
                            tags.append(Tag(tagType=entity.label_, value=entity.text))

                pred.nlu = nlu_pred
                # The DP model will need to have the NLU intent prediction to make its own
                # action prediction.
                conv.turns[-1].userAction.intent = nlu_pred.intent.value

        if self._do_dp:
            # Predict the next agent action to take.
            dp_preds = self._dp_model.predict(convs)
            for pred, dp_pred in zip(predictions, dp_preds):
                pred.dp = dp_pred

        return ChatbotPipelinePredictions(predictions=predictions)

    def _detect_conv_language(self, conv: Conversation) -> t.Optional[str]:
        """
        Combines all user utterances into one string to detect the language robustly.
        """

        user_utterances = ''
        for turn in conv.turns:
            if turn.actor == Actor.USER:
                utterance = turn.userAction.utterance
                if utterance:
                    user_utterances += utterance + '\n'

        if user_utterances:
            doc = self.spacy_en(user_utterances)
            return doc._.language.get('language')
        return
