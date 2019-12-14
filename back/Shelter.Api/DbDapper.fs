module DbDapper
// this is based on fsharp-dapper lib https://github.com/AlexTroshkin/fsharp-dapper

open System
open System.Runtime.Serialization
open FSharp.Data.Dapper
open System.Data.SQLite

module Connection =
    let mkShared () = 
        let dbPath = __SOURCE_DIRECTORY__ + @"\..\shelter.db"
        let conn = new SQLiteConnection ("Data Source=" + dbPath + ";New=False;Version=3;Compress=True;")
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
    let CreateGem title text = querySingleAsync<int> {
        let conn = connectionF ()
        let cmd = new SQLiteCommand("begin", conn)
        parameters (dict [
            "Title", box title; 
            "Text", box text; 
            "CreationDate", box DateTime.Now; 
            "LastUpdateDate", box DateTime.Now])
        script "insert into Gems (Title, Text, CreationDate, LastUpdateDate) VALUES (@Title, @Text, @CreationDate, @LastUpdateDate);
                select seq from sqlite_sequence where name='Gems'"
    }
