
class record_class:
    area: str
    domain: str
    article_heading: str
    section_heading : str
    chapter : str
    section : str
    article : str
    paragraph : str
    point: str
    sub_point : str
    related_to: str
    responsible: str
    stipulation: str
    full_text : str

class DataRecord:
    @classmethod
    def from_row(cls, row):
        instance = cls()
        for key, value in row.items():
            setattr(instance, key.lower(), value)
        return instance
    

dora_properties_params = """
                            supported_on: $supported_on
                            , domain: $domain 
                            , article_heading: article_heading
                            , section_heading : $section_heading
                            , chapter : $chapter 
                            , section : $section
                            , article : $article
                            , paragraph : $paragraph
                            , point: $point
                            , sub_point : $sub_point
                            , related_to: $related_to
                            , responsible: $responsible
                            , stipulation: $stipulation
                            , full_text : $full_text
                            """

create_dora_record_file = """
                create (n:Record_File)
                set n += {{ {properties}, ctInsert: datetime() }} 
                return n
                """




"""
// supported_on and domain
match (n:Record_File)
with collect(distinct n.supported_on) as lsupported_on, collect(distinct n.domain) as ldomain
unwind lsupported_on as supported_on
merge (so:Supported_on {name:supported_on})
with ldomain
match (n:Record_File)
match (so:Supported_on where so.name = n.supported_on)
merge (so)-[:SUPPORTED_ON]->(n)
// domain
with ldomain
unwind ldomain as domain
merge (dm:Domain {name:domain})
with ldomain
match (n:Record_File)
match (dm:Domain) where dm.name = n.domain
merge (dm)-[:DOMAIN]->(n)
// articulo -> n
with distinct n.article as article, n.article_heading as article_heading
merge (ar:Article {name:article_heading, ID: article})
with ar
match (n:Record_File)
match (ar:Article) where ar.ID = n.article
merge (ar)-[:ARTICLE]->(n)
with n, ar
match (n)<-[:SUPPORTED_ON]-(sp:Supported_on)
create (p:Paragraph {art_ID:ar.ID, par_ID: toInteger(n.paragraph), point: toString(n.point), sub_point:n.sub_point})
set p.full_text = n.full_text
    , p.related_to = n.related_to
    , p.responsible = n.responsible
    , p.stipulation = n.stipulation
merge (p)<-[:SUPPORTED_ON]-(sp)
with p, ar
//match (ar:Article {ID:p.art_ID})
merge (ar)-[:FULL_TEXT]->(p)

// rs -responsible
with p
with collect(distinct p.responsible) as lresponsible
    , collect(distinct p.related_to) as lrelated_to
    , collect(distinct p.stipulation) as lstipulation
unwind lresponsible as responsible
merge (rs:Responsible {name:responsible})

with rs, lstipulation, lrelated_to
match (p:Paragraph {responsible:rs.name})
merge (p)<-[:RESPONSIBLE]-(rs)

// related_to
with lrelated_to, lstipulation
unwind lrelated_to as related_to
merge (rt:Related_to {name:related_to})

with rt, lstipulation
match (p:Paragraph {related_to:rt.name})
merge (p)<-[:RELATED_TO]-(rt)

// stipulation
with lstipulation
unwind lstipulation as stipulation
merge (st:Stipulation {name:stipulation})

with st
match (p:Paragraph {stipulation:st.name})
merge (p)<-[:STIPULATION]-(st)


return distinct "succesful process" as result

"""

"""
// so->articulo 
match (n:Record_File)<-[:ARTICLE]-(ar:Article)
match (so:Supported_on)-[:SUPPORTED_ON]->(n)
merge (so)-[:SUPPORTED_ON]->(ar)

with n, ar
match (dm:Domain)-[:DOMAIN]->(n)
merge (dm)-[:DOMAIN]->(ar)

// borrar
with n
detach delete n


"""

create_root =   """
                MERGE (N:NIST {ID:'NIST'})
                on create set N.ctInsert = datetime()
                on match set N.ctUpdate = datetime()
                set N.name = 'NIST'
                WITH N
                MERGE (NP:NIST_Publication {ID:'NIST 800-53 R5'})
                on create set NP.ctInsert = datetime()
                on match set NP.ctUpdate = datetime()
                set NP.name = 'NIST Special Publication 800-53 release 5'
                WITH N,NP
                MERGE (N)-[R:PUBLICATION]->(NP)
                on create set R.ctInsert = datetime()
                on match set R.ctUpdate = datetime()
                WITH NP
                MATCH (C:Category)
                MERGE (C)<-[RCP:CATEGORY_PUB]-(NP)
                on create set RCP.ctInsert = datetime()
                on match set RCP.ctUpdate = datetime()
                RETURN C,NP
                """

