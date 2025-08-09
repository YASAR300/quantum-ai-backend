import random
from ..config import settings
from ..utils.logger import logger

def refine_probability_with_quantum(p: float) -> float:
    try:
        if not settings.ENABLE_QUANTUM:
            raise RuntimeError("Quantum disabled")
        noise = (0.5 - abs(p-0.5)) * 0.1 * (1 if random.random()>0.5 else -1)
        p_ref = max(0.0, min(1.0, p + noise))
        logger.info(f"[Quantum] refined {p:.3f}->{p_ref:.3f}")
        return p_ref
    except Exception as e:
        logger.warning(f"[Quantum Fallback] {e}")
        p_ref = max(0.0, min(1.0, p * 0.98 + 0.01))
        return p_ref

def blend(ai_p: float, q_p: float) -> float:
    a = settings.QUANTUM_BLEND_ALPHA
    return max(0.0, min(1.0, a*ai_p + (1-a)*q_p))
