{% set film_title = 'The Matrix' %}


SELECT *
FROM {{ ref('films') }}
WHERE title = '{{ film_title }}'
