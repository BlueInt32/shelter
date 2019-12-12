open System
open FSharp.Data.Sql

[<Literal>]
let ResolutionPath = __SOURCE_DIRECTORY__ + "/libraries/"

[<Literal>] // Relative to resolutionPath:
let ConnStr = @"Filename=" + __SOURCE_DIRECTORY__ + @"/../shelter.db"

// In case of dependency error, note that SQLite dependencies are processor architecture dependant
type HR = SqlDataProvider< Common.DatabaseProviderTypes.SQLITE, ConnStr, ResolutionPath = ResolutionPath, SQLiteLibrary=Common.SQLiteLibrary.MicrosoftDataSqlite>

[<EntryPoint>]
let main argv =
    let ctx = HR.GetDataContext()
    let employeesFirstName =
        query {
            for emp in ctx.Main.Gems do
            select emp.Title
        } |> Seq.head

    printfn "Hello %s!" employeesFirstName
    0 // return an integer exit code
