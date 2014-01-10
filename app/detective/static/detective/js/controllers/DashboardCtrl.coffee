class DashboardCtrl
    # Injects dependancies
    @$inject: ['$scope', '$routeParams', 'Common', 'Page', 'User', '$location']

    constructor: (@scope,  @routeParams, @Common, @Page, @User,  @location)->
        @Page.loading no
        @Page.title "Your dashboard"

        @scope.selectedModels = []
        # We received a model to add to the list
        @scope.dropModel = (data, ev)=>
            # We want to add an element
            if data["json/adding"]?
                name = data["json/adding"]
                # If the model isn't selected yet...
                unless _.findWhere @scope.selectedModels, {name: name}
                    # Add the model to the list
                    @scope.selectedModels.push
                        name: name
                        top:  ev.layerY
                        left: ev.layerX

        # Get the topics of the current user
        @scope.userTopics = @Common.get type: "topic", author__username: @User.username

angular.module('detective').controller 'dashboardCtrl', DashboardCtrl