class ArticleCtrl
    # Injects dependancies
    @$inject: ['$scope', '$routeParams', 'Common', 'Page']

    constructor: (@scope,  @routeParams, @Common, @Page)->
        # Enable loading mode
        @Page.loading yes
        # ──────────────────────────────────────────────────────────────────────
        # Scope attributes
        # ──────────────────────────────────────────────────────────────────────
        # Get the data from the database
        params =
            type       : "article"
            slug       : @routeParams.slug
            topic__slug: @routeParams.topic
        @Common.query params, (articles)=>
            # Disable loading mode
            @Page.loading no
            # Stop if it's an unkown topic or article
            return @scope.is404(yes) unless articles.length
            # Or take the article at the top of the list
            @scope.article = articles[0]

angular.module('detective.controller').controller 'articleCtrl', ArticleCtrl