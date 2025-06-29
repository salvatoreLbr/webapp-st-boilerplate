from enum import Enum


class Role(Enum):
    USER = 1
    USER_ADMIN = 2
    ADMIN = 3


class AuthManager:
    """
    Gestisce i livelli di autorizzazione richiesti per ciascun metodo della classe Cmd.
    """

    def __init__(self):
        # Mappa i nomi dei metodi della classe Cmd al livello di autorizzazione minimo richiesto.
        self._method_permissions: dict[str, int] = {
            "backup_db": Role.USER_ADMIN,
            "create_user": Role.ADMIN,
            "disable_user": Role.ADMIN,
            "get_user": Role.USER,
            "update_user": Role.USER,
            # Aggiungi qui tutti gli altri metodi della tua classe Cmd
        }

    def get_required_level(self, method_name: str) -> Role:
        """
        Restituisce il livello di autorizzazione minimo richiesto per un dato metodo.

        Args:
            method_name (str): Il nome del metodo della classe Cmd.

        Returns:
            int: Il livello di autorizzazione minimo richiesto.
                Restituisce un livello più alto del massimo (es. Role.ADMIN + 1)
                se il metodo non è mappato, per default negare l'accesso.
        """
        return self._method_permissions.get(method_name, Role.ADMIN.value + 1)

    def can_access(self, user_current_level: int, method_name: str) -> bool:
        """
        Verifica se l'utente con il livello corrente può accedere al metodo.

        Args:
            user_current_level (int): Il livello di autorizzazione dell'utente corrente.
            method_name (str): Il nome del metodo della classe Cmd.

        Returns:
            bool: True se l'utente ha il permesso, False altrimenti.
        """
        required_level = self.get_required_level(method_name)
        return user_current_level >= required_level.value
