"""Extra visual vanish effects and gesture classifiers for VanishCam."""

from __future__ import annotations

import math
import cv2
import numpy as np


class ParticleSystem:
    """Disperses the person's silhouette into drifting wind particles."""

    def __init__(self, frame: np.ndarray, mask: np.ndarray, step: int = 5):
        self.step = step
        # Sample points within the person's silhouette
        ys, xs = np.where(mask[::step, ::step] > 0.40)
        self.xs = (xs * step).astype(np.float32)
        self.ys = (ys * step).astype(np.float32)

        if len(self.xs) > 0:
            # Sample original frame colors at those points
            valid_y = np.clip(self.ys.astype(int), 0, frame.shape[0] - 1)
            valid_x = np.clip(self.xs.astype(int), 0, frame.shape[1] - 1)
            self.colors = frame[valid_y, valid_x]

            rng = np.random.default_rng(12345)
            # Wind drifts to the right with slight turbulence
            self.vx = rng.uniform(160, 420, size=len(self.xs)).astype(np.float32)
            self.vy = rng.uniform(-80, 50, size=len(self.xs)).astype(np.float32)
            self.phase = rng.uniform(0, 2 * math.pi, size=len(self.xs)).astype(np.float32)
        else:
            self.colors = np.zeros((0, 3), dtype=np.uint8)
            self.vx = np.zeros(0, dtype=np.float32)
            self.vy = np.zeros(0, dtype=np.float32)
            self.phase = np.zeros(0, dtype=np.float32)

    def render(self, background: np.ndarray, progress: float) -> np.ndarray:
        if len(self.xs) == 0 or progress >= 0.99:
            return background.copy()

        h, w = background.shape[:2]
        s = self.step
        out = background.copy()

        # Update positions
        t = progress * 2.2
        cur_x = (self.xs + self.vx * t).astype(np.int32)
        cur_y = (self.ys + self.vy * t + 15 * np.sin(t * 6 + self.phase)).astype(np.int32)

        valid = (cur_x >= 0) & (cur_x < w - s) & (cur_y >= 0) & (cur_y < h - s)
        if not np.any(valid):
            return out

        cur_x = cur_x[valid]
        cur_y = cur_y[valid]
        colors = self.colors[valid]

        min_x, max_x = max(0, cur_x.min()), min(w, cur_x.max() + s)
        min_y, max_y = max(0, cur_y.min()), min(h, cur_y.max() + s)

        patch_h = max_y - min_y
        patch_w = max_x - min_x
        if patch_h <= 0 or patch_w <= 0:
            return out

        layer = np.zeros((patch_h, patch_w, 3), dtype=np.uint8)
        mask_l = np.zeros((patch_h, patch_w), dtype=np.uint8)

        rel_x = cur_x - min_x
        rel_y = cur_y - min_y

        for x, y, c in zip(rel_x, rel_y, colors):
            layer[y:y+s, x:x+s] = c
            mask_l[y:y+s, x:x+s] = 255

        alpha = max(0.0, 1.0 - progress)
        m = (mask_l[:, :, None].astype(np.float32) / 255.0) * alpha
        crop_bg = out[min_y:max_y, min_x:max_x]
        out[min_y:max_y, min_x:max_x] = (
            layer.astype(np.float32) * m + crop_bg.astype(np.float32) * (1.0 - m)
        ).astype(np.uint8)

        return out


def apply_glitch(
    frame: np.ndarray,
    background: np.ndarray,
    mask: np.ndarray,
    progress: float,
) -> np.ndarray:
    """Cyberpunk holographic glitch and digital scanlines deactivation."""
    if progress >= 0.99:
        return background.copy()

    points = cv2.findNonZero((mask > 0.05).astype(np.uint8))
    if points is None:
        return background.copy()

    x, y, w, h = cv2.boundingRect(points)
    left, top = max(0, x - 15), max(0, y - 15)
    right, bottom = min(frame.shape[1], x + w + 15), min(frame.shape[0], y + h + 15)

    glitched = frame[top:bottom, left:right].copy()
    crop_mask = mask[top:bottom, left:right].copy()

    # Flickering holographic alpha
    flicker = 0.5 + 0.5 * math.sin(progress * 30.0)
    alpha = (1.0 - progress) * (0.6 + 0.4 * flicker)
    alpha_map = crop_mask[:, :, None] * alpha

    # Chromatic aberration (RGB shift)
    shift = int(14 * (1.0 - progress))
    if shift > 0 and glitched.shape[1] > shift * 2:
        glitched[:, :-shift, 0] = glitched[:, shift:, 0]  # Blue shift
        glitched[:, shift:, 2] = glitched[:, :-shift, 2]  # Red shift

    # Digital horizontal line tearing
    rng = np.random.default_rng(int(progress * 50))
    gh, gw = glitched.shape[:2]
    for _ in range(5):
        ys = rng.integers(0, max(1, gh - 15))
        hs = rng.integers(4, 16)
        dx = rng.integers(-35, 35)
        glitched[ys:ys+hs] = np.roll(glitched[ys:ys+hs], dx, axis=1)

    # Scanlines
    glitched[::3, :, :] = (glitched[::3, :, :] * 0.55).astype(np.uint8)

    # Cyan holographic edge
    edge = cv2.Canny((crop_mask * 255).astype(np.uint8), 80, 180)
    if np.any(edge):
        cyan_glow = cv2.dilate(edge, np.ones((3, 3), np.uint8), iterations=1)
        glitched[cyan_glow > 0] = [255, 230, 80]

    out = background.copy()
    crop_bg = out[top:bottom, left:right]
    out[top:bottom, left:right] = np.clip(
        glitched.astype(np.float32) * alpha_map
        + crop_bg.astype(np.float32) * (1.0 - alpha_map),
        0, 255
    ).astype(np.uint8)

    return out


def is_finger_extended(points: np.ndarray, base: int) -> bool:
    """True if fingertip distance from wrist is significantly greater than PIP joint."""
    tip = points[base + 3]
    joint = points[base + 1]
    wrist = points[0]
    return float(np.linalg.norm(tip - wrist)) > float(np.linalg.norm(joint - wrist)) * 1.15


def is_open_palm(points: np.ndarray) -> bool:
    """Recognize open palm facing camera (all 5 fingers spread)."""
    if points.shape[0] < 21:
        return False
    # 4 main fingers extended
    all_four = all(is_finger_extended(points, b) for b in (5, 9, 13, 17))
    if not all_four:
        return False
    # Thumb tip also extended outward
    thumb_tip = points[4]
    thumb_mcp = points[2]
    wrist = points[0]
    thumb_ext = float(np.linalg.norm(thumb_tip - wrist)) > float(np.linalg.norm(thumb_mcp - wrist)) * 1.10
    return thumb_ext


def is_thumbs_up(points: np.ndarray) -> bool:
    """Recognize thumbs-up gesture (4 fingers folded, thumb pointing up)."""
    if points.shape[0] < 21:
        return False
    # 4 fingers folded
    folded = [not is_finger_extended(points, b) for b in (5, 9, 13, 17)]
    if not all(folded):
        return False
    # Thumb tip pointing up above thumb MCP
    # (in normalized/image space, lower y is higher)
    return points[4, 1] < points[2, 1] - 0.04

