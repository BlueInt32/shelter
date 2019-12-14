module Db

open System
open Microsoft.EntityFrameworkCore
open System.Runtime.Serialization
open Shelter.Domain

// inspired by the article by the bald guy https://www.eelcomulder.nl/2018/03/16/using-entity-framework-core-with-f/
// github repo : https://github.com/EelcoMulder/EFCoreWithFSharp/tree/master/EFCore.App

type GemContext = 
    inherit DbContext
    new() = { inherit DbContext() }
    new(options: DbContextOptions<GemContext>) = { inherit DbContext(options) }

    // override __.OnModelCreating modelBuilder = 
        // let esconvert = ValueConverter<EpisodeStatus, string>((fun v -> v.ToString()), (fun v -> Enum.Parse(typedefof<EpisodeStatus>, v) :?> EpisodeStatus))
        // modelBuilder.Entity<Gem>().Property(fun e -> e.Status).HasConversion(esconvert) |> ignore

        //let ssconvert = ValueConverter<SerieStatus, string>((fun v -> v.ToString()), (fun v -> Enum.Parse(typedefof<SerieStatus>, v) :?> SerieStatus))
        //modelBuilder.Entity<Serie>().Property(fun e -> e.Status).HasConversion(ssconvert) |> ignore      


    [<DefaultValue>]
    val mutable gems:DbSet<Gem>
    member x.Gems 
        with get() = x.gems 
        and set v = x.gems <- v

    //[<DefaultValue>]
    //val mutable episodes:DbSet<Episode>
    //member x.Episodes 
    //    with get() = x.episodes 
    //    and set v = x.episodes <- v    



let _getGemById (context: GemContext) id =
    query {
        for serie in context.Gems do
            where (serie.Id = id)
            select serie 
            exactlyOne
    } |> (fun x -> if box x = null then None else Some x)

let _getGems (context: GemContext) =
    query {
        for serie in context.Gems do
            select serie 
    } |> (fun x -> if box x = null then None else Some x)
    

let _createGemAsync (context: GemContext) (gemTitle: string) (gemText: string) =
    async {
        let entity = { Id= 0; Title = gemTitle; Text = gemText; CreationDate = DateTime.Now; LastUpdateDate = DateTime.Now }
        (context.Gems.AddAsync entity).AsTask () |> Async.AwaitTask |> ignore
        let! _ = context.SaveChangesAsync true |> Async.AwaitTask
        return entity
    }

let _createGem (context: GemContext) (gemTitle: string) (gemText: string) =
    let entity = { Id= 0; Title = gemTitle; Text = gemText; CreationDate = DateTime.Now; LastUpdateDate = DateTime.Now }
    context.Gems.Add(entity) |> ignore
    context.SaveChanges true |> ignore
    entity


let configureSqliteContext = 
    (fun () ->
        let optionsBuilder = new DbContextOptionsBuilder<GemContext>();
        let dbPath = __SOURCE_DIRECTORY__ + @"\..\shelter.db;"
        optionsBuilder.UseSqlite(@"Data Source="+ dbPath)|> ignore
        new GemContext(optionsBuilder.Options)
    )



let getContext = configureSqliteContext()
let getGemById  = _getGemById getContext
let getGems  = _getGems getContext
let createGem = _createGem getContext
let createGemAsync = _createGemAsync getContext
//let getEpisode = SerieRepository.getEpisode getContext
//let getEpisodeLinq = SerieRepository.getEpisode getContext
//let addSerie = SerieRepository.addSerie getContext
//let addSerieAsync = SerieRepository.addSerieAsync getContext
//let updateSerie = SerieRepository.updateSerie getContext
//let deleteSerie = SerieRepository.deleteSerie getContext
//let getSeriesWithAiredEpisodes = SerieRepository.getSeriesWithAiredEpisodes getContext
