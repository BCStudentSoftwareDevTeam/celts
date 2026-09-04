from peewee import fn
from playhouse.shortcuts import model_to_dict
from app.models.user import User
def searchUsers(query, category=None):
    '''
        Search the User table based on the search query and category

        MySQL LIKE is case insensitive
    '''
    splitSearch = query.strip().split()
    if not splitSearch:
        return User.select().where(False)
    searchWhere = None
    for namePart in splitSearch:
        nameSearch = namePart + "%"
        namePartWhere = (
            User.firstName.contains(namePart) | User.lastName.contains(namePart) | User.username.contains(namePart))
        if searchWhere is None:
            searchWhere = namePartWhere
        else:
            searchWhere &= namePartWhere

    if category == "instructor":
        userWhere = (User.isFaculty | User.isStaff)
    elif category == "admin":
        userWhere = (User.isCeltsAdmin)
    elif category == "studentstaff":
        userWhere = (User.isCeltsStudentStaff)
    elif category == "operationsTeam":
        userWhere = (User.isCeltsOperationsTeam)
    elif category == "celtsLinkAdmin":
        userWhere = (User.isFaculty | User.isStaff | User.isCeltsStudentStaff | User.isCeltsOperationsTeam)
    elif category == "all":
        userWhere = (True)
    else:
        userWhere = (User.isStudent)

    fullSearchText = " ".join(splitSearch)
    # Combine into query
    searchResults = User.select().where(searchWhere, userWhere).order_by(
        fn.CONCAT(User.firstName, " ", User.lastName).contains(fullSearchText).desc(),
        User.firstName.startswith(fullSearchText).desc(),
        User.lastName.startswith(fullSearchText).desc(),
        User.lastName,
        User.firstName
    )

    return { user.username : model_to_dict(user) for user in searchResults }
