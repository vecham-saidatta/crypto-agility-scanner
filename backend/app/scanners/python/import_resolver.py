import ast


class ImportResolver:
    """
    Resolves imported symbols while respecting simple
    source-order name shadowing.
    """

    def resolve(
        self,
        tree: ast.AST,
    ) -> dict[str, list[tuple[int, str | None]]]:

        symbols: dict[str, list[tuple[int, str | None]]] = {}

        for node in ast.walk(tree):

            # import hashlib
            # import hashlib as hl
            if isinstance(node, ast.Import):

                for alias in node.names:

                    local_name = alias.asname or alias.name

                    symbols.setdefault(
                        local_name,
                        [],
                    ).append(
                        (
                            node.lineno,
                            alias.name,
                        )
                    )

            # from hashlib import md5
            if isinstance(node, ast.ImportFrom):

                if node.module is None:
                    continue

                for alias in node.names:

                    local_name = alias.asname or alias.name

                    symbols.setdefault(
                        local_name,
                        [],
                    ).append(
                        (
                            node.lineno,
                            f"{node.module}.{alias.name}",
                        )
                    )

            # def md5(...):
            #
            # A local function now shadows an imported symbol.
            if isinstance(
                node,
                (ast.FunctionDef, ast.AsyncFunctionDef),
            ):

                symbols.setdefault(
                    node.name,
                    [],
                ).append(
                    (
                        node.lineno,
                        None,
                    )
                )

            # class AES:
            #
            # Classes can shadow imported names too.
            if isinstance(node, ast.ClassDef):

                symbols.setdefault(
                    node.name,
                    [],
                ).append(
                    (
                        node.lineno,
                        None,
                    )
                )

        # ast.walk() isn't guaranteed to represent our
        # symbol history in the order we want to query it.
        for history in symbols.values():
            history.sort(
                key=lambda item: item[0]
            )

        return symbols