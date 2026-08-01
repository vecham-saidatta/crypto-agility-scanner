from app.scanners.findings import Finding


class AlgorithmInventory:
    """
    Builds an inventory of detected cryptographic algorithms.
    """

    def generate(
        self,
        findings: list[Finding],
    ) -> dict[str, int]:

        inventory: dict[str, int] = {}

        for finding in findings:

            algorithm = finding.algorithm

            inventory[algorithm] = (
                inventory.get(algorithm, 0) + 1
            )

        return inventory
