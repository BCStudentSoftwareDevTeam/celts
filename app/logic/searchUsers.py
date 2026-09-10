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
        # This individual search term can match the user's first name, last name, or username.
        namePartWhere = (User.firstName.contains(namePart) | User.lastName.contains(namePart) | User.username.contains(namePart))
        # For the first search term, initialize the WHERE condition.
        if searchWhere is None:
            searchWhere = namePartWhere
        else:
            searchWhere &= namePartWhere # Require every search term to match at least one of the first name, last name, or username fields.

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
    elif category == "currentStudents":
        userWhere = (User.rawClassLevel.in_(["Freshman", "Sophomore", "Junior", "Senior"]))
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
