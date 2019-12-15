module Db

open InputModels
open LiteDB
open LiteDB.FSharp
open System

let mapper = FSharpBsonMapper()
let liteDbPath = __SOURCE_DIRECTORY__ + "/../shelter_litedb.db"

type Genre = Rock | Pop | Metal

[<CLIMutable>]
type Gem = {
    Id: int
    Title: string
    Text: string
    CreationDate: DateTime
    LastUpdateDate: DateTime
}

let createGem (inputModel:GemInputModel) =
    use db = new LiteDatabase(liteDbPath, mapper)
    let gems = db.GetCollection<Gem>("gems")
    let newGem = {
        Id = 0;
        Title = inputModel.title;
        Text = inputModel.text;
        CreationDate = DateTime.Now;
        LastUpdateDate = DateTime.Now; }
    // gems.EnsureIndex(fun x -> x.Title, true) |> ignore
    gems.Insert(newGem) |> ignore
    newGem

let getGems =
    use db = new LiteDatabase(liteDbPath, mapper)
    let gems = db.GetCollection<Gem>("gems")
    let result = gems.FindAll ()
    result
