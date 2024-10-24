def new_customer_recommender(item_id: int, items_purchased: list[list[int]]) -> list[int]:
    """Returns a list of items that users also bought along with the currently viewed item 
    Args:
        item_id int : Item a user is currently viewing  
        items_purchased list[list[int]] : Purchases previous customers have made 
        
    Returns:
        list[int]: Items that customers bought along with item currently being viewed   
    """
    recommendations = []
    for i in items_purchased:
        if item_id in i:
            recommendations +=i
    # Eliminate the item customer is currently viewing
    # & Make sure all items are unique 
    recommendations = list(set(recommendations) - set([item_id]))
    return recommendations[:5]