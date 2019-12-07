open Suave
open Suave.Successful
open Suave.Operators
open Suave.Filters
open Suave.Json
open Shed.Domain
open Suave.Utils.Collections
open Suave.Writers

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


//let allowCors : WebPart =
//    choose [
//        POST >=> setCORSHeaders 
//    ]
let webPart = 
    choose [
        OPTIONS >=> setCORSHeaders >=> OK "CORS approved"
        path "/api" >=> GET >=> warbler (fun _ -> Db.getGems () |> Api.toJson |> OK)
        path "/api/gems" >=> choose [
            POST >=> setCORSHeaders >=> createGem
        ]
        path "/api/hello" >=> choose [
            GET  >=> request (fun r -> OK (greetings r.query))
            POST >=> request (fun r -> OK (greetings r.form))
            RequestErrors.NOT_FOUND "Found no handlers" ]
        pathScan "/api/gems/%d" 
            (fun id -> OK (sprintf "Post details: %d" id))

    ]
    >=> Suave.Writers.setMimeType "application/json; charset=utf-8"

startWebServer config webPart
