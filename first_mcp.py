# simple_server.py
from mcp.server.fastmcp import FastMCP

# Créer un serveur MCP
mcp = FastMCP("Mon Premier Serveur MCP")


# Ajouter un outil pour obtenir des informations utilisateur
@mcp.tool()
def get_user_context(id: int) -> dict:
    """
    Obtenir les informations sur un utilisateur par son ID

    Parameters:
        id: L'identifiant numérique de l'utilisateur à rechercher

    Returns:
        Un dictionnaire contenant les informations de l'utilisateur
    """
    # On mock le retour d'une API/BDD
    return {"id": id, "name": "Jean Mahmoud", "age": 40, "hobbies": "Danse avec les stars"}


# Ajouter un outil pour obtenir le solde bancaire
@mcp.tool()
def get_user_money() -> dict:
    """Obtenir le solde des comptes bancaires de l'utilisateur"""
    # On mock le retour d'une API/BDD
    return {"bank1": -100, "bank2": 60}
