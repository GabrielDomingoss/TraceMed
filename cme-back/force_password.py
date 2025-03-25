from database import SessionLocal
from models.user import User
from utils.auth import get_password_hash

db = SessionLocal()

email = "joao@hospital.com"
new_password = get_password_hash("teste123")

user = db.query(User).filter(User.email == email).first()

if user:
    user.password = new_password
    db.commit()
    print("Senha atualizada com sucesso.")
else:
    print("Usuário não encontrado.")

db.close()
