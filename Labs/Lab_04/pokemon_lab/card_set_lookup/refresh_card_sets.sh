#!/bin/bash
set -e 

echo "Refeshing all card sets in the $card_sets_dir directory..."

for FILE in "$card_sets_dir"/*.json; do
    SET_ID=$(basename "$FILE" .json)
    echo "Refreshing card set: $SET_ID"
    curl -s "https://api.pokemontcg.io/v2/cards?q=set.id:${SET_ID}" -o "$FILE"
    echo "Updated data is written to $FILE and is done"
done


echo "All card sets have been refreshed."