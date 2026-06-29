const typesenseInstantsearchAdapter = new TypesenseInstantSearchAdapter({
    server: {
      apiKey: "9B1PUuRZU5szyFE6HZGRHi19f03aWIql",
      nodes: [
        {
          host: "typesense.acdh-dev.oeaw.ac.at",
          port: "443",
          protocol: "https",
        },
      ],
      cacheSearchResultsForSeconds: 2 * 60
    },
    additionalSearchParameters: {
      query_by: "full_text"
    },
  });

const projcetLabels = {
  "nbr-pius-xi": "Nuntiatur Pius XI",
  "tillich-briefe": "Tillich Briefe",
  "nbr-graz": "Digitale Edition Grazer Nuntiaturberichte (1580-[1602])",  
  "gtrans": "Die Große Transformation",  
  "tillich-lectures": "Tillich Lectures",
  "grundbuecher": "Wiener Grundbücher (1438–1473)",
  "schnitzler-briefe": "Schnitzler-Briefe",
  "Schnitzler-Zeitungen": "Schnitzler-Zeitungen",
  "Schnitzler-Mikrofilme": "Schnitzler-Mikrofilme",  
  "schnitzler-kino": "Schnitzler-Kino",
  "schnitzler-interviews": "Schnitzler-Interviews",
  "rita": "Reading in the Alps",
  "sbt": "Schnitzler-Tagebuch",
  "STB": "Staribacher Tagebuch",
  "bahr-static": "Bahr-Schnitzler-Briefwechsel",
  "hbtv": "Bahr-Textverzeichnis",
  "legalkraus": "Rechtsakten Karl Kraus",
  "akademie-static": "Edition Akademieprotokolle",
  "thun-static": "Thun-Korrespondenz",
  "abcd-db": "Anton Bruckner Chronologie Datenbank",
  "ablo": "Anton Bruckner-Lexikon online",
  "ficker-briefe": "Ludwig Ficker Gesamtbriefwechsel",
  "mrp": "Die Ministerratsprotokolle 1848–1918",
  "staribacher": "Tagebuch Josef Staribacher: Digitale Edition",
  "fackel-texte": "Die Texte der 'Fackel'",
  "oebl": "Österreichisches Biographisches Lexikon",
  "pollaczek": "Clara Katharina Pollaczek – Arthur Schnitzler und ich",
  "freud-edition": "Sigmund Freuds Werke",
  "amp": "Auden-Musulin-Papers",
  "emt": "Kaiserin Eleonora Magdalena Korrespondenz",
  "oeml": "Österreichisches Musiklexikon Online",
  "hsl": "Hanslick Online",
  "gestrich_index": "Gestrich Index",
};

const blacklistedProjectFacets = new Set([
  "staribacher",
  "gestrich_index"
]);


const searchClient = typesenseInstantsearchAdapter.searchClient;
const search = instantsearch({
    indexName: 'cfts',
    searchClient,
});

search.addWidgets([
    instantsearch.widgets.searchBox({
        container: '#searchbox',
        cssClasses: {
          form: 'form-inline',
          input: 'form-control col-md-11',
          submit: 'btn btn-primary',
          reset: 'btn btn-primary'
        },
    }),

    instantsearch.widgets.hits({
        container: '#hits',
        transformItems(items) {
          console.log(items)
          return items.map(item => ({
            ...item,
            project: projcetLabels[item.project],
            persons: [...new Set(item.persons)],
            places: [...new Set(item.places)],
            works: [...new Set(item.works)]
          }));
        },
        templates: {
            empty: 'Keine Ergebnisse',
            item: `
                <h3><a href="{{ resolver }}">{{ title }}</a></h3>
                <h5><span class="badge bg-primary text-white">{{ project }}</span></h5>
                <div>
                {{#persons}}
                <span class="badge bg-secondary text-white">{{ . }}</span>
                {{/persons}}
                </div>
                <div>
                {{#places}}
                <span class="badge bg-info text-white">{{ . }}</span>
                {{/places}}
                </div>
                {{#works}}
                <span class="badge bg-success text-white">{{ . }}</span>
                {{/works}}
                </div>
                </div>
                {{#keywords}}
                <span class="badge bg-success text-white">{{ . }}</span>
                {{/keywords}}
                </div>
                <p>{{#helpers.snippet}}{ "attribute": "full_text" }{{/helpers.snippet}}</p>
            `
        }
    }),

    instantsearch.widgets.stats({
        container: '#stats-container',
        templates: {
          text: `
            {{#areHitsSorted}}
              {{#hasNoSortedResults}}Keine Treffer{{/hasNoSortedResults}}
              {{#hasOneSortedResults}}1 Treffer{{/hasOneSortedResults}}
              {{#hasManySortedResults}}{{#helpers.formatNumber}}{{nbSortedHits}}{{/helpers.formatNumber}} Treffer {{/hasManySortedResults}}
              aus {{#helpers.formatNumber}}{{nbHits}}{{/helpers.formatNumber}}
            {{/areHitsSorted}}
            {{^areHitsSorted}}
              {{#hasNoResults}}Keine Treffer{{/hasNoResults}}
              {{#hasOneResult}}1 Treffer{{/hasOneResult}}
              {{#hasManyResults}}{{#helpers.formatNumber}}{{nbHits}}{{/helpers.formatNumber}} Treffer{{/hasManyResults}}
            {{/areHitsSorted}}
            gefunden in {{processingTimeMS}}ms
          `,
        }
    }),

    instantsearch.widgets.refinementList({
        container: '#refinement-list-places',
        attribute: 'places',
        searchable: true,
        cssClasses: {
          searchableInput: 'form-control form-control-sm mb-2 border-light-2',
          searchableSubmit: 'd-none',
          searchableReset: 'd-none',
          showMore: 'btn btn-secondary btn-sm align-items-center',
          list: 'list-unstyled',
          count: 'badge bg-light text-dark ms-2',
          label: 'd-flex align-items-center text-capitalize',
          checkbox: 'me-2',
        }
    }),
    instantsearch.widgets.refinementList({
      container: '#refinement-list-keywords',
      attribute: 'keywords',
      searchable: true,
      cssClasses: {
        searchableInput: 'form-control form-control-sm mb-2 border-light-2',
        searchableSubmit: 'd-none',
        searchableReset: 'd-none',
        showMore: 'btn btn-secondary btn-sm align-items-center',
        list: 'list-unstyled',
        count: 'badge bg-light text-dark ms-2',
        label: 'd-flex align-items-center text-capitalize',
        checkbox: 'me-2',
      }
  }),

    instantsearch.widgets.refinementList({
      container: '#refinement-list-project',
      attribute: 'project',
      searchable: true,
      limit: 100,
      transformItems(items) {
        return items
          .filter((item) => !blacklistedProjectFacets.has(item.value))
          .map(item => ({
            ...item,
            highlighted: projcetLabels[item.value] || item.label
          }));
      },
      cssClasses: {
        searchableInput: 'form-control form-control-sm mb-2 border-light-2',
        searchableSubmit: 'd-none',
        searchableReset: 'd-none',
        showMore: 'btn btn-secondary btn-sm align-items-center',
        list: 'list-unstyled',
        count: 'badge bg-light text-dark ms-2',
        label: 'd-flex align-items-center text-capitalize',
        checkbox: 'me-2',
      }
  }),

    instantsearch.widgets.refinementList({
        container: '#refinement-list-persons',
        attribute: 'persons',
        searchable: true,
        cssClasses: {
          searchableInput: 'form-control form-control-sm mb-2 border-light-2',
          searchableSubmit: 'd-none',
          searchableReset: 'd-none',
          showMore: 'btn btn-secondary btn-sm align-items-center',
          list: 'list-unstyled',
          count: 'badge bg-light text-dark ms-2',
          label: 'd-flex align-items-center text-capitalize',
          checkbox: 'me-2',
        }
    }),

    instantsearch.widgets.refinementList({
        container: '#refinement-list-works',
        attribute: 'works',
        searchable: true,
        cssClasses: {
          searchableInput: 'form-control form-control-sm mb-2 border-light-2',
          searchableSubmit: 'd-none',
          searchableReset: 'd-none',
          showMore: 'btn btn-secondary btn-sm align-items-center',
          list: 'list-unstyled',
          count: 'badge bg-light text-dark ms-2',
          label: 'd-flex align-items-center text-capitalize',
          checkbox: 'me-2',
        }
    }),
    
    instantsearch.widgets.rangeInput({
        container: "#range-input",
        attribute: "year",
        cssClasses: {
          form: 'form-inline',
          input: 'form-control',
          submit: 'btn btn-primary'
        }
      }),

    instantsearch.widgets.pagination({
        container: '#pagination',
        padding: 2,
        cssClasses: {
          list: 'pagination',
          item: 'page-item',
          link: 'page-link'
        }
    }),
    instantsearch.widgets.clearRefinements({
        container: '#clear-refinements',
        cssClasses: {
          button: 'btn btn-primary'
        }
    }),

    	

    instantsearch.widgets.currentRefinements({
      container: '#current-refinements',
      excludedAttributes: ['project'],
      cssClasses: {
        delete: 'btn btn-primary',
        label: 'badge'
      }
    })
]);


search.addWidgets([
    instantsearch.widgets.configure({
        attributesToSnippet: ['full_text'],
    })
]);

search.addWidgets([
    instantsearch.widgets.sortBy({
      container: "#sort-by",
      items: [
        { label: "Tag (aufsteigend)", value: "cfts/sort/date:asc" },
        { label: "Tag (absteigend)", value: "cfts/sort/date:desc" },
        { label: "Jahr (aufsteigend)", value: "cfts/sort/year:asc" },
        { label: "Jahr (absteigend)", value: "cfts/sort/year:desc" },
      ],
      cssClasses: {
        select: 'form-select'
      }
    }),
  ]);


search.start();
