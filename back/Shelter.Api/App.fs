open HttpUtilities
open Suave
open Suave.Successful
open Suave.Operators
open Suave.Filters
open Suave.Json
open Shelter.Domain
open InputModels
open FSharp.Data.Dapper
open DbDapper

let config = 
    { defaultConfig with
        bindings = [ HttpBinding.createSimple HTTP "127.0.0.1" 5001 ]
    }

let webPart = 
    choose [
        OPTIONS >=> setCORSHeaders >=> OK "CORS approved"
        path Path.Gems.overview >=>
            GET >=> warbler (fun _ -> Async.RunSynchronously DbDapper.getAllGems |> Api.toJson |> OK)
        path Path.Gems.creation >=>
            POST_CORS 
            >=> mapJsonSbu
                (fun (gemInputModel:GemInputModel) -> Async.RunSynchronously (DbDapper.CreateGem gemInputModel.title gemInputModel.text))
        //pathScan Path.Gems.details 
        //    (fun id -> Db.getGemById id |> Api.toJson |> OK)

    ]
    >=> Suave.Writers.setMimeType "application/json; charset=utf-8"

// fshard-dapper specifics, so that the fields with the Option type are treated like Nullable
OptionHandler.RegisterTypes()


startWebServer config webPart
