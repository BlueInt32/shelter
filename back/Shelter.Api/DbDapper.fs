module DbDapper
// this is based on fsharp-dapper lib https://github.com/AlexTroshkin/fsharp-dapper

open System
open System.Runtime.Serialization
open FSharp.Data.Dapper
open Microsoft.Data.Sqlite

module Connection =
    let mkShared () = 
        let dbPath = __SOURCE_DIRECTORY__ + @"\..\shelter.db;"
        let conn = new SqliteConnection ("Data Source=" + dbPath)
        conn

[<DataContract>]
type [<CLIMutable>] Gem =
    {
        [<field: DataMember(Name = "id")>]
        Id: int
        [<field: DataMember(Name = "title")>]
        Title: string
        [<field: DataMember(Name = "text")>]
        Text: string
        [<field: DataMember(Name = "creationDate")>]
        CreationDate: DateTime
        [<field: DataMember(Name = "lastUpdateDate")>]
        LastUpdateDate: DateTime
    }

module DbDapper =
    let private connectionF () = 
        let conn = Connection.SqliteConnection (Connection.mkShared())
        Console.WriteLine(conn.ToString())
        conn

    let querySeqAsync<'R>          = querySeqAsync<'R> (connectionF)
    let querySingleAsync<'R>       = querySingleAsync<'R> (connectionF)
    let querySingleOptionAsync<'R> = querySingleOptionAsync<'R> (connectionF)


    let getAllGems = querySeqAsync<Gem> {
        // parameters (dict ["Login", box login])
        script "select * from Gems"
    }

    let findByIDs identificators = querySeqAsync<Gem> {
        values "GemId" identificators 
        script """
            select *
            from Gems as g
                join GemId as gid on
                    g.Id = gid.Value
        """
    }
