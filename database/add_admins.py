
from app.models.user import User

for username in ["ramsayb2", "heggens", "rohrers", "lyonss", "cochranea"]:
    User.update(isCeltsAdmin=True).where(User.username == username).execute()
