class IndividualSingleCtrl
    # Injects dependancies    
    @$inject: ['$scope', '$routeParams', 'Individual', 'Summary', '$filter', '$anchorScroll', '$location', 'Page']

    constructor: (@scope, @routeParams, @Individual, @Summary, @filter, @anchorScroll, @location, @Page)->      
        @scope.get        = (n)=> @scope.individual[n] or false if @scope.individual?
        @scope.hasRels    = @hasRels  
        @scope.isLiteral  = @isLiteral
        @scope.isString   = (t)=> ["CharField", "URLField"].indexOf(t) > -1
        @scope.isRelationship = (d) => ["Relationship", "ExtendedRelationship"].indexOf(d.type) > -1
        @scope.scrollTo   = @scrollTo  
        @scope.singleUrl  = @singleUrl
        @scope.strToColor = @filter("strToColor")
        # ──────────────────────────────────────────────────────────────────────
        # Scope attributes
        # ──────────────────────────────────────────────────────────────────────  
        # Read route params
        @scope.scope = @routeParams.scope
        @scope.type  = @routeParams.type
        @scope.id    = @routeParams.id
        # Get individual from database
        @Individual.get type: @scope.type, id: @scope.id, (data)=> 
            @scope.individual = data
            # Set page's title
            @Page.setTitle @filter("individualPreview")(data)
        # Get meta information for this type
        @Summary.get id: "forms", (data)=> @scope.meta = data[@scope.type.toLowerCase()]        
        

    hasRels: ()=> 
        if @scope.meta? and @scope.individual?
            _.some @scope.meta.fields, (field)=> 
                @scope.isRelationship(field)  and @scope.individual[field.name].length

    scrollTo: (id)=> 
        @location.hash(id)
        @anchorScroll()
    singleUrl: (individual, type=false)=> 
        type = (type or @scope.type).toLowerCase()
        "/node/#{type}/#{individual.id}/"
    # True if the given type is literal
    isLiteral: (field)=>
        [
            "CharField",
            "DateTimeField",
            "URLField",
            "IntegerField"
            "AutoField"
        ].indexOf(field.type) > -1
    
angular.module('detective').controller 'individualSingleCtrl', IndividualSingleCtrl
