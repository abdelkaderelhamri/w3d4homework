import requests

MISSING_IMAGE_URL = "https://tinyurl.com/missing-tv"
TVMAZE_API_URL = "http://api.tvmaze.com/"

shows_list = []
episodes_list = []
episodes_area = []
search_form = []


def get_shows_by_term(term):
    response = requests.get(f"{TVMAZE_API_URL}search/shows", params={"q": term})
    results = response.json()

    shows = []
    for result in results:
        show = result["show"]
        image_url = show["image"]["medium"] if show["image"] else MISSING_IMAGE_URL
        shows.append({
            "id": show["id"],
            "name": show["name"],
            "summary": show["summary"],
            "image": image_url
        })

    return shows


def populate_shows(shows):
    shows_list.clear()

    for show in shows:
        show_markup = f"""
        <div data-show-id="{show['id']}" class="Show col-md-12 col-lg-6 mb-4">
           <div class="media">
             <img src="{show['image']}" alt="{show['name']}" class="w-25 me-3">
             <div class="media-body">
               <h5 class="text-primary">{show['name']}</h5>
               <div><small>{show['summary']}</small></div>
               <button class="btn btn-outline-light btn-sm Show-getEpisodes">
                 Episodes
               </button>
             </div>
           </div>
        </div>
      """

        shows_list.append(show_markup)


def search_for_show_and_display():
    term = search_form["term"]
    shows = get_shows_by_term(term)

    episodes_area.clear()
    populate_shows(shows)


def get_episodes_of_show(show_id):
    response = requests.get(f"{TVMAZE_API_URL}shows/{show_id}/episodes")
    episodes = response.json()

    episodes_list = []
    for episode in episodes:
        episodes_list.append({
            "id": episode["id"],
            "name": episode["name"],
            "season": episode["season"],
            "number": episode["number"]
        })

    return episodes_list


def populate_episodes(episodes):
    episodes_list.clear()

    for episode in episodes:
        episode_markup = f"""
        <li>
            {episode['name']}
            (season {episode['season']}, episode {episode['number']})
        </li>
        """

        episodes_list.append(episode_markup)

    episodes_area = True


def get_episodes_and_display(evt):
    show_id = evt.target.closest(".Show").dataset["show-id"]

    episodes = get_episodes_of_show(show_id)
    populate_episodes(episodes)


search_form.on("submit", search_for_show_and_display)
shows_list.on("click", ".Show-getEpisodes", get_episodes_and_display)