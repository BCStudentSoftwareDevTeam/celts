from peewee import fn
from playhouse.shortcuts import model_to_dict
from app.models.user import User
def searchUsers(query, category=None):
    '''
        Search the User table based on the search query and category

        MySQL LIKE is case insensitive
    '''
    # add wildcards to each piece of the query
    splitSearch = query.strip().split()
    if not splitSearch:
        return User.select().where(False)
    fullSearch = " ".join(splitSearch) + "%"
    searchWhere = (User.firstName ** fullSearch | User.lastName ** fullSearch | User.username ** fullSearch)
    for splitIndex in range(1, len(splitSearch)):
        firstName = " ".join(splitSearch[:splitIndex]) + "%"
        lastName = " ".join(splitSearch[splitIndex:]) + "%"

        searchWhere |= (
            (User.firstName ** firstName) &
            (User.lastName ** lastName)
        )

    # Also allow individual pieces of the name to match
    for namePart in splitSearch:
        nameSearch = namePart + "%"

        searchWhere |= (
            (User.firstName ** nameSearch) |
            (User.lastName ** nameSearch) |
            (User.username ** nameSearch)
        )
    
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
        fn.CONCAT(User.firstName, " ", User.lastName)
            .contains(fullSearchText)
            .desc(),
        User.firstName.startswith(fullSearchText).desc(),
        User.lastName.startswith(fullSearchText).desc(),
        User.lastName,
        User.firstName
    )

    return { user.username : model_to_dict(user) for user in searchResults }
