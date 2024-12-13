def is_valid_voter_id(voter_id: str) -> bool:
    '''
    Validates that the Voter ID is alphanumeric and at least 3 characters long.
    '''
    return len(voter_id) >= 3 and voter_id.isalnum()
