from ..config import settings
from ..utils.logger import logger
from ..ml.model import load_model, top_feature_importance
from ..ml.preprocess import EXPECTED_FEATURES

def quantum_feature_mask(num_features: int) -> list[int]:
    """
    Quantum-inspired feature selection:
    - Keep top-K important features from the trained model
    - Ensure we always keep at least `min_keep` features
    - Fallback to keeping all features on any error
    """
    try:
        if not settings.ENABLE_QUANTUM:
            raise RuntimeError("Quantum disabled")

        model = load_model()
        if model is None:
            raise RuntimeError("Model not trained yet")

        # how many to keep
        min_keep = 5  # you can tweak this
        k = max(min_keep, num_features // 2)
        k = min(k, num_features)  # never exceed total features

        # get top-k features by LR coefficient magnitude
        fi_list = top_feature_importance(model, k=k) or []
        top_features = [item["feature"] for item in fi_list if "feature" in item]

        # if something went wrong, keep all
        if not top_features:
            logger.warning("[Quantum] top_features empty; keeping all features.")
            return [1] * num_features

        # build mask in EXPECTED_FEATURES order
        keep_set = set(top_features)
        mask = [1 if f in keep_set else 0 for f in EXPECTED_FEATURES[:num_features]]

        # safety: avoid degenerate mask (all 0s)
        if sum(mask) == 0:
            logger.warning("[Quantum] mask became all zeros; forcing all ones.")
            mask = [1] * num_features

        logger.info(f"[Quantum] Selected top features: {top_features}")
        logger.info(f"[Quantum] Feature mask: {mask}")
        return mask

    except Exception as e:
        logger.warning(f"[Quantum Fallback] {e}")
        return [1] * num_features  # fallback → keep all
