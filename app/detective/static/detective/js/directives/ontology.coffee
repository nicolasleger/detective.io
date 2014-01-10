angular.module("detective").directive "ontology", ["$timeout", ($timeout)->
    restrict: 'E'
    link: (scope, elem, attrs, ctrl) ->
        plumb = jsPlumb.getInstance
            Connector    : [ "Bezier", curviness: 10 ]
            Endpoint     : [ "Dot", radius: 5 ]
            EndpointStyle: fillStyle: "#aaa"
            Anchor       : "AutoDefault"
            PaintStyle   :
                lineWidth   : 2
                strokeStyle : "#aaa"
                outlineWidth: 0
        # Watch the given object
        scope.$watch attrs.ngModel, ->
            # Add a short delay to be sure that the elments are rendered
            $timeout ->
                # For each registered model...
                _.each scope[attrs.ngModel], (m, idx)->
                    # Find the element where create an endpoint
                    elm = elem.find("[data-id='#{m.name}']")
                    # Make it draggable
                    plumb.draggable elm, containment: elem
                    # Add drag&drop connexion ability
                    plumb.addEndpoint elm, isSource: yes, isTarget: yes
            , 400

        , yes # Deep inspection
]