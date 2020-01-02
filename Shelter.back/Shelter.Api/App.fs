open HttpUtilities
open Suave
open Suave.Successful
open Suave.Operators
open Suave.Filters
open Suave.Json
open Shelter.Domain
open InputModels

let config = 
    { defaultConfig with
        bindings = [ HttpBinding.createSimple HTTP "127.0.0.1" 5001 ]
    }

let gemsCreateHandler = fun (gemInputModel:GemInputModel) -> Db.createGem gemInputModel
let gemsGetHandler = fun _ -> Db.getGems
let tagsCreateHandler = fun (tagInputModel:TagInputModel) -> Db.createTag tagInputModel
let webPart = 
    choose [
        OPTIONS >=> setCORSHeaders >=> OK "CORS approved"
        path Path.Gems.create 
            >=> POST_CORS >=> mapJsonSbu 
            gemsCreateHandler        
        path Path.Gems.search 
            >=> POST_CORS >=> mapJsonSbu
            gemsGetHandler
        path Path.Tags.create 
            >=> POST_CORS >=> mapJsonSbu
            tagsCreateHandler
    ]
    >=> Suave.Writers.setMimeType "application/json; charset=utf-8"

startWebServer config webPart
