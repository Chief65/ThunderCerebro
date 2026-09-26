{% if config("developerMode") == "enabled" %}

const iconsConfig = {
    "header": "Category Icons",
    "options": [
        {% for category in store.categories %}
        {
            "id": "icon-{{ category.id }}",
            "name": "{{ category.name }}",
            "description": "Upload an icon for {{ category.name }}",
            "type": "image-uploader"
        }
        {%- if not loop.last -%},{% endif %}    
        {% endfor %}{% if store.pages | length > 0 %},{% endif %}
        
        {% for page in store.pages %}
        {
            "id": "icon-{{ page.slug }}",
            "name": "{{ page.title }}",
            "description": "Upload an icon for {{ page.title }}",
            "type": "image-uploader"
        }
        {%- if not loop.last -%}
        ,
        {% endif %}
        {% endfor %}
    ]
}



$("body").prepend(`

<pre>
${JSON.stringify(iconsConfig, null, '\t')}
</pre>
`)
{% endif %}