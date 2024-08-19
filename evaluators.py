import logging
from mlflow.metrics.genai import EvaluationExample, faithfulness, relevance

def create_faithfulness_metric():
    logging.info("Creating faithfulness metric")
    faithfulness_examples = [
        EvaluationExample(
            input="How do I disable MLflow autologging?",
            output="mlflow.autolog(disable=True) will disable autologging for all functions. In Databricks, autologging is enabled by default. ",
            score=2,
            justification="The output provides a working solution, using the mlflow.autolog() function that is provided in the context.",
            grading_context={
                "context": "mlflow.autolog(log_input_examples: bool = False, log_model_signatures: bool = True, log_models: bool = True, log_datasets: bool = True, disable: bool = False, exclusive: bool = False, disable_for_unsupported_versions: bool = False, silent: bool = False, extra_tags: Optional[Dict[str, str]] = None) → None[source] Enables (or disables) and configures autologging for all supported integrations. The parameters are passed to any autologging integrations that support them. See the tracking docs for a list of supported autologging integrations. Note that framework-specific configurations set at any point will take precedence over any configurations set by this function."
            },
        ),
        EvaluationExample(
            input="How do I disable MLflow autologging?",
            output="mlflow.autolog(disable=True) will disable autologging for all functions.",
            score=5,
            justification="The output provides a solution that is using the mlflow.autolog() function that is provided in the context.",
            grading_context={
                "context": "mlflow.autolog(log_input_examples: bool = False, log_model_signatures: bool = True, log_models: bool = True, log_datasets: bool = True, disable: bool = False, exclusive: bool = False, disable_for_unsupported_versions: bool = False, silent: bool = False, extra_tags: Optional[Dict[str, str]] = None) → None[source] Enables (or disables) and configures autologging for all supported integrations. The parameters are passed to any autologging integrations that support them. See the tracking docs for a list of supported autologging integrations. Note that framework-specific configurations set at any point will take precedence over any configurations set by this function."
            },
        ),
    ]
    return faithfulness(model="openai:/gpt-4", examples=faithfulness_examples)

def create_relevance_metric():
    logging.info("Creating relevance metric")
    return relevance(model="openai:/gpt-4")
