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

let webPart = 
    choose [
        OPTIONS >=> setCORSHeaders >=> OK "CORS approved"
        path Path.Gems.creation >=> POST_CORS >=> mapJsonSbu
            (fun (gemInputModel:GemInputModel) -> Db.createGem gemInputModel)
        path Path.Gems.searchForGems >=> POST_CORS >=> mapJsonSbu
            (fun _ -> Db.getGems)
//        path Path.Gems.creation >=>            POST_CORS 
//            >=> mapJsonSbu
//                (fun (gemInputModel:GemInputModel) -> Async.RunSynchronously (Db.createGemAsync gemInputModel))
//        pathScan Path.Gems.details 
//            (fun id -> Db.getGemById id |> Api.toJson |> OK)

    ]
    >=> Suave.Writers.setMimeType "application/json; charset=utf-8"

startWebServer config webPart
