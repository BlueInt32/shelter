module DataAccess

open System.IO
open NPoco
open Microsoft.Data.Sqlite

module GemsAccess = 
    type Gem() =
        member val ID = 0 with get, set
        member val Name = "" with get, set
        member val Latitude = 0.0 with get, set
        member val Longitude = 0.0 with get, set
        member val Cuisine = "" with get, set
        member val VegetarianOptions = false with get, set
        member val VeganOptions = false with get, set

    [<CLIMutable>]
    type GemFilter =
        { Cool: Option<string>
          Nice: Option<bool> }

    let private connString = "Filename=" + __SOURCE_DIRECTORY__+ "/../shelter.db"


    let private getFetchingQuery filter =
        let coolPart, hasCool =
            match filter.Cool with
            | Some c -> (sprintf "Cuisine = \"%s\"" c, true)
            | None -> ("", false)

        let nicePart, hasNicePart =
            match filter.Nice with
            | Some v -> (sprintf "VegetarianOptions = \"%d\"" (if v then 1 else 0), true) // Sqlite uses ints 0 and 1 for bools.
            | None -> ("", false)

        let hasWhereClause = hasCool || hasNicePart 

        let query = 
            "select * from Gems" + 
            (if hasWhereClause then " where " else "") +
            coolPart +
            (if hasCool && hasNicePart then " and " + nicePart else nicePart)

        query

    let getGems (filter: GemFilter) =
        let query = getFetchingQuery filter

        use conn = new SqliteConnection(connString)
        conn.Open()

        use db = new Database(conn)
        db.Fetch<Gem>(query)
