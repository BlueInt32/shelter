module Path

type IntPath = PrintfFormat<(int -> string), unit, string, string, int>

let home = "/"

module Gems = 
    let overview = "/api/gems"
    let search = "/api/gems/search"
    let create = "/api/gems"
    let tests = "/api/tests"
    let details : IntPath = "/api/gems/%d"

module Tags = 
    let create = "/api/tags"
    let search = "/api/tags/search"

