module Domain

open LiteDB
open LiteDB.FSharp


[<CLIMutable>]
type Tag = {
    Id: int
    Label: string
}

[<CLIMutable>]
type Gem = {
    Id: int
    Title: string
    Text: string
    CreationDate: System.DateTime
    LastUpdateDate: System.DateTime
    Tags: List<Tag>
}

let mapper = FSharpBsonMapper()
mapper.DbRef<Gem,_>(fun g -> g.Tags)
