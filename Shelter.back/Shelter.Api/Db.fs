module Db

open InputModels
open LiteDB
open LiteDB.FSharp
open Domain
open System.Linq

let mapper = FSharpBsonMapper()
let liteDbPath = __SOURCE_DIRECTORY__ + "/../../db/shelter.lite.db"

type QueryResult<'a> =
    | Success of 'a
    | DatabasePathError of System.ArgumentNullException
    
let createGem (inputModel:GemInputModel) =
    try
        use db = new LiteDatabase(liteDbPath, mapper)
        let dbTags = db.GetCollection<Tag>("tags")
        let dbGems = db.GetCollection<Gem>("gems")
        let allTags = dbTags.FindAll ()
        
        let getMaybeExistingTag label = 
            allTags |> Seq.tryFind (fun dbTag -> dbTag.Label = label)
        
        let createTag label =
            let newTag = { Id = 0; Label = label }
            dbTags.Insert(newTag) |> ignore
            newTag

        let createOrRetrieveTag label = 
            match (getMaybeExistingTag label) with
            | Some existingTag -> existingTag
            | _ -> createTag label

        let gemsTags = inputModel.tags |> Seq.map createOrRetrieveTag

        let newGem = {
            Id = 0;
            Title = inputModel.title;
            Text = inputModel.text;
            CreationDate = System.DateTime.Now;
            LastUpdateDate = System.DateTime.Now;
            Tags = List.ofSeq gemsTags }
        let x = dbGems.Insert(newGem) 
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


let createTag (inputModel:TagInputModel) =
    try
        use db = new LiteDatabase(liteDbPath, mapper)
        let tags = db.GetCollection<Tag>("tags")
        let tag = {
            Id = 0;
            Label = "music" 
        }
        tags.Insert(tag) |> ignore
        let newTag = {
            Id = 0;
            Label = inputModel.label;
        }
        tags.Insert(newTag) |> ignore
        Success newTag
    with
        | :? System.ArgumentNullException as ex ->
             DatabasePathError ex
        | _ ->                    // don't handle any other cases
            reraise()

let searchForTags (inputModel:TagsSearchInputModel) =
    try
        use db = new LiteDatabase(liteDbPath, mapper)
        let tags = db.GetCollection<Tag>("tags")
        let result = tags.Find (fun tag -> tag.Label.StartsWith inputModel.labelSearchText)

        Success (result.Take inputModel.limit)
    with 
        | :? System.ArgumentNullException as ex ->
             DatabasePathError ex
        | _ ->                    // don't handle any other cases
            reraise()
