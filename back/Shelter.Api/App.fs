open Suave
open Suave.Successful
open Suave.Operators
open Suave.Filters
open Suave.Json
open Shelter.Domain
open Suave.Utils.Collections
open Suave.Writers
open System.Runtime.Serialization

let createGem = (mapJson (fun (a:string) -> { bar = a }))

let config = 
    { defaultConfig with
        bindings = [ HttpBinding.createSimple HTTP "127.0.0.1" 5001 ]
    }

let greetings q =
  defaultArg (Option.ofChoice (q ^^ "name")) "World" |> sprintf "Hello %s"

let setCORSHeaders =
    setHeader "Access-Control-Allow-Origin" "*"
    >=> setHeader "Access-Control-Allow-Headers" "content-type"

[<DataContract>]
type GemInputModel =
  { 
    [<field: DataMember(Name = "title")>]
    title : string 
    [<field: DataMember(Name = "text")>]
    text : string 
  }

let mapJsonAsync (f: 'a -> Async<'b>) =
  fun (ctx : HttpContext) ->
    async{
      let! result = f (fromJson ctx.request.rawForm)
      return Successful.ok (toJson result ) ctx >>= Writers.setMimeType "application/json"
    }
    
let webPart = 
    choose [
        OPTIONS >=> setCORSHeaders >=> OK "CORS approved"
        path Path.Gems.overview >=> GET >=> warbler (fun _ -> Db.getGems |> Api.toJson |> OK)
        path Path.Gems.creation >=> POST >=> setCORSHeaders 
            >=> (mapJsonWith fromJson Api.toJsonBytes (fun (gemInputModel:GemInputModel) -> Async.RunSynchronously (Db.createGemAsync gemInputModel.title gemInputModel.text)))
        pathScan Path.Gems.details 
            (fun id -> Db.getGemById id |> Api.toJson |> OK)

    ]
    >=> Suave.Writers.setMimeType "application/json; charset=utf-8"

startWebServer config webPart
