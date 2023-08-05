import torch


def dice_loss(input: torch.Tensor,
              target: torch.Tensor,
              epsilon: float = 0.) -> torch.Tensor:
    r"""
    Dice loss defined in the V-Net paper as:
    Loss_dice = 1 - D
            2 * sum(p_i * g_i) + epsilon
    D = ---------------------------------------
         sum(p_i ^ 2) + sum(g_i ^ 2) + epsilon
    where the sums run over the N mask pixels (i = 1 ... N), of the predicted binary segmentation
    pixel p_i ∈ P and the ground truth binary pixel g_i ∈ G.

    Args:
        input (Tensor): predicted binary mask, each pixel value should be in range [0, 1].
        target (Tensor): ground truth binary mask.

    Returns:
        Tensor: dice loss.
    """
    assert input.shape[-2:] == target.shape[-2:]
    input = input.view(input.size(0), -1).float()
    target = target.view(target.size(0), -1).float()

    loss = 1 - \
        (2 * torch.sum(input * target, dim=1) + epsilon) / \
        (torch.sum(input * input, dim=1) + torch.sum(target * target, dim=1) + 1e-4 + epsilon)

    return loss
