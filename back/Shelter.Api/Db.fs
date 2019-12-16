module Db

open InputModels
open LiteDB
open LiteDB.FSharp
open Domain

let mapper = FSharpBsonMapper()
let liteDbPath = __SOURCE_DIRECTORY__ + "/../../db/shelter.lite.db"

type QueryResult<'a> =
    | Success of 'a
    | DatabasePathError of System.ArgumentNullException
    
let createGem (inputModel:GemInputModel) =
    try
        use db = new LiteDatabase(liteDbPath, mapper)
        let gems = db.GetCollection<Gem>("gems")
        let newGem = {
            Id = 0;
            Title = inputModel.title;
            Text = inputModel.text;
            CreationDate = System.DateTime.Now;
            LastUpdateDate = System.DateTime.Now; }
        // gems.EnsureIndex(fun x -> x.Title, true) |> ignore
        gems.Insert(newGem) |> ignore
        raise (new System.ArgumentNullException("yolo"))
        Success newGem
    with
        | :? System.ArgumentNullException as ex ->
             DatabasePathError ex
        | _ ->                    // don't handle any other cases
            reraise()

let getGems =
    try
        use db = new LiteDatabase(liteDbPath, mapper)
        let gems = db.GetCollection<Gem>("gems")
        let result = gems.FindAll ()
        Success result
    with 
        | :? System.ArgumentNullException as ex ->
             DatabasePathError ex
        | _ ->                    // don't handle any other cases
            reraise()
