import bcrypt

def generar_hash_contrasena(contrasena: str) -> str:
    contrasena_bytes = contrasena.encode("utf-8")

    # bcrypt admite hasta 72 bytes (si no, falla)
    if len(contrasena_bytes) > 72:
        raise ValueError("La contrasena supera 72 bytes. Usa una mas corta.")

    hash_bytes = bcrypt.hashpw(contrasena_bytes, bcrypt.gensalt())
    return hash_bytes.decode("utf-8")

def verificar_contrasena(contrasena: str, hash_guardado: str) -> bool:
    return bcrypt.checkpw(contrasena.encode("utf-8"), hash_guardado.encode("utf-8"))