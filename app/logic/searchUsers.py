from playhouse.shortcuts import model_to_dict
from app.models.user import User
def searchUsers(query, category=None):
    '''
        Search the User table based on the search query and category

        MySQL LIKE is case insensitive
    '''
    # add wildcards to each piece of the query
    splitSearch = query.strip().split()
    firstName = splitSearch[0] + "%"
    lastName = " ".join(splitSearch[1:]) +"%"

    if len(splitSearch) == 1: # search for query in first OR last name
        searchWhere = (User.firstName ** firstName | User.lastName ** firstName | User.username ** splitSearch)
    else:                     # search for first AND last name
        searchWhere = (User.firstName ** firstName & User.lastName ** lastName)

    if category == "instructor":
        userWhere = (User.isFaculty | User.isStaff)
    elif category == "admin":
        userWhere = (User.isCeltsAdmin)
    elif category == "studentstaff":
        userWhere = (User.isCeltsStudentStaff)
    elif category == "celtsLinkAdmin":
        userWhere = (User.isFaculty | User.isStaff | User.isCeltsStudentStaff)
    else:
        userWhere = (User.isStudent)

    # Combine into query
    searchResults = User.select().where(searchWhere, userWhere)

    return { user.username : model_to_dict(user) for user in searchResults }
