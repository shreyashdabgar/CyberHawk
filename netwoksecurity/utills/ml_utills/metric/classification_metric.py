from netwoksecurity.entities.artifact_entity import classifiactionmetricartifact
from netwoksecurity.logging.logger import logging
from netwoksecurity.exception.exception import CustomException
from sklearn.metrics import f1_score, precision_score, recall_score

def get_classfiaction_score(y_true, y_pred) -> classifiactionmetricartifact:
    try :
        model_f1_score = f1_score(y_true, y_pred) 
        model_recall_score = recall_score(y_true, y_pred)
        model_precision_score = precision_score(y_true, y_pred)

        classification_metric_artifact = classifiactionmetricartifact(
            f1_score=model_f1_score,
            precision_score=model_precision_score,
            recall_score=model_recall_score
        )
        return classification_metric_artifact
    
    except CustomException as e :
        raise CustomException(e)
