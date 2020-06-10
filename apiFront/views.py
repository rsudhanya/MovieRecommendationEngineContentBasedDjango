from django.shortcuts import render

# Create your views here.

def index(request):
    from django.conf import settings
    import os
    import pandas as pd
    movie_data_frame = pd.read_pickle(os.path.join(settings.BASE_DIR, "movie_data_frame.pkl"))

    try:
        currentPage = int(request.GET.get("p"))
    except:
        currentPage = 1

    try:
        movie_to_rec = request.GET.get("moviename")

        def get_row_from_index(index):
            return movie_data_frame[movie_data_frame.index == index]
        def get_index_from_title(title):
            return movie_data_frame[movie_data_frame.title == title]["index"].values[0]
        
        movie_index = get_index_from_title(movie_to_rec)

        import numpy
        similarity_score = numpy.load(os.path.join(settings.BASE_DIR, "similarity_score.npy"))
        similar_movies = list(enumerate(similarity_score[movie_index]))
        sorted_similar_movies_index = sorted(similar_movies, key=lambda x: x[1], reverse=True)

        similar_movies_data_frame = map(lambda element: get_row_from_index(element[0]), sorted_similar_movies_index[currentPage * 10 - 10 : currentPage * 10 - 1])
        
        responseDic = {"movies_similar": similar_movies_data_frame, "pages": range(1, len(sorted_similar_movies_index) // 10), "currentPage": currentPage, "moviename": movie_to_rec}
    except Exception as ex:
        print(ex)
        search = request.GET.get("search")
        if search != None:
            movie_data_frame = movie_data_frame[movie_data_frame['title'].str.contains(search, case=False)]
        responseDic = {"movies": movie_data_frame.sort_values(by=['title'])[currentPage * 10 - 10 : currentPage * 10 - 1].iterrows(), "pages": range(1, movie_data_frame.shape[0] // 10), "currentPage": currentPage, "search": search}
        
    return render(request, 'apiFront/index.html', responseDic)


def about(request):
    return render(request, 'apiFront/about.html')