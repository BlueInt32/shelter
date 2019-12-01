open Suave.Web
open Suave
open Suave.Filters
open Suave.Successful
open Suave.Operators
open Suave.Json
open Shed.Domain
open Suave.Utils.Collections

let createPost = (mapJson (fun (a:Foo) -> { bar = a.foo }))

let config = 
    { defaultConfig with
        bindings = [ HttpBinding.createSimple HTTP "127.0.0.1" 5001 ]
    }

let greetings q =
  defaultArg (Option.ofChoice (q ^^ "name")) "World" |> sprintf "Hello %s"

let webPart = 
    choose [
        path "/" >=> GET >=> warbler (fun _ -> Db.getGems () |> Api.toJson |> OK)
        path "/gems" >=> choose [
            POST >=> createPost
        ]
        path "/hello" >=> choose [
            GET  >=> request (fun r -> OK (greetings r.query))
            POST >=> request (fun r -> OK (greetings r.form))
            RequestErrors.NOT_FOUND "Found no handlers" ]
        pathScan "/gems/%d" 
            (fun id -> OK (sprintf "Post details: %d" id))

    ]
    >=> Suave.Writers.setMimeType "application/json; charset=utf-8"

startWebServer config webPart
