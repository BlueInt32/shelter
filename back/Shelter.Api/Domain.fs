module Domain

[<CLIMutable>]
type Gem = {
    Id: int
    Title: string
    Text: string
    CreationDate: System.DateTime
    LastUpdateDate: System.DateTime
}

