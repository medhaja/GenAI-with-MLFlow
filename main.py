import pandas as pd
import mlflow
import logging
from utils import load_documents, split_documents
from models import create_embeddings, create_faiss_index, create_qa_chain
from evaluators import create_faithfulness_metric, create_relevance_metric

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def model(input_df, qa):
    answer = []
    for index, row in input_df.iterrows():
        answer.append(qa(row["questions"]))
    return answer

def main():
    logging.info("Starting the main function")

    # Load and split documents
    logging.info("Loading documents from 'operating system.pdf'")
    documents = load_documents("operating system.pdf")
    logging.info("Splitting documents into chunks")
    texts = split_documents(documents)

    # Create embeddings and FAISS index
    logging.info("Creating embeddings")
    embeddings = create_embeddings()
    logging.info("Creating FAISS index from documents")
    docsearch = create_faiss_index(texts, embeddings)

    # Create QA chain
    logging.info("Creating QA chain")
    qa = create_qa_chain(docsearch)

    # Wrapper function to pass qa to the model
    def model_wrapper(input_df):
        return model(input_df, qa)

    # Evaluation data
    logging.info("Preparing evaluation data")
    eval_df = pd.DataFrame(
        {
            "questions": [
                "What is Memory protection in Paged Environment?",
                "How to prevent Deadlock?",
                "what is Hierarchical Page table?",
                "what is VIRTUAL MEMORY?",
            ],
        }
    )

    # Create metrics
    logging.info("Creating faithfulness metric")
    faithfulness_metric = create_faithfulness_metric()
    logging.info("Creating relevance metric")
    relevance_metric = create_relevance_metric()

    # Evaluate model
    logging.info("Evaluating the model")
    results = mlflow.evaluate(
        model_wrapper,
        eval_df,
        model_type="question-answering",
        evaluators="default",
        predictions="result",
        extra_metrics=[faithfulness_metric, relevance_metric, mlflow.metrics.latency()],
        evaluator_config={
            "col_mapping": {
                "inputs": "questions",
                "context": "source_documents",
            }
        },
    )

    logging.info("Evaluation results:")
    logging.info(results.metrics)
    logging.info(results.tables["eval_results_table"])

if __name__ == "__main__":
    main()
