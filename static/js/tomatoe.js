
var Query = Backbone.Model.extend({
	
	/*
	 * 	{
	 * 	
	 * 		states : [],	
	 * 		fields : []
	 * }
	*/

	reset : function(){
		this.set("states",[]);
		this.set("fields",[]);
	},
	
	addState : function(state){
		var currentStates = this.get("states");
		if(undefined == currentStates) currentStates = [];
		
		currentStates.push(state);
		this.set({states : currentStates});
		this.trigger("states-changed");
	},
	
	setStates : function(states){
		this.set({states : states});
		this.trigger("states-changed");
	},
	
	removeState : function(state){
		var currentStates = this.get("states");
		if(undefined == currentStates) currentStates = [];
		
		currentStates = _.reject(currentStates, function(s){ return s == state; }); 
		this.set({states : currentStates});
		this.trigger("states-changed");
	},
	
	addField : function(field){
		var currentFields = this.get("fields");
		if(undefined == currentFields) currentFields = [];
		
		currentFields.push(field);
		this.set({fields : currentFields});
		this.trigger("fields-changed");
	},
	
	setFields : function(fields){
		this.set({fields : fields});
		this.trigger("fields-changed");
	},
	
	removeField : function(field){
		var currentFields = this.get("fields");
		if(undefined == currentFields) currentFields = [];
		
		
		
		currentFields = _.reject(currentFields, function(s){ return s == field; }); 
		this.set({fields : currentFields});
		this.trigger("fields-changed");
	},
	
	toString : function(){
		var fields = _.reduce(this.get("fields"), function(memo, field){ return memo + field + ","; }, "fields=");
		var states = _.reduce(this.get("states"), function(memo, state){ return memo + state + ","; }, "states=");
		
		if(fields.length > 1){
			fields = fields.substring(0,fields.length-1);
		}
		
		if(states.length > 1){
			states = states.substring(0,states.length-1);
		}
		
		return fields + "&" + states;
	},
	
	isComplete : function(){
		var fields = this.get("fields");
		var states = this.get("states");
		
		if( (fields == undefined) || (states == undefined)) return false; 
		if( (fields.length == 0) || (states.length == 0)) return false;
		
		return true;
	}
	
});

var Dataset = Backbone.Model.extend({
  
		  /* 
		  *   {
		  * 	columns : [
		  * 		{ title : "", description : "" }
		  * 	],
		  * 
		  * 	data : [
		  * 		[col1, col2, col3, ....],
		  * 	]
		  *   } 
		  * 
		  */
 		  url : function(){
 		  	return "/datafeed?" + this.get("query");
 		  }	
	}
);

var DataSnapshot = Backbone.Model.extend({
		/*
		 *  {
		 * 	  title : "", 
		 * 	  fields : ["field1", "field2", "field2"]
		 *  }
		*/
});

var DataSnapshotCollection = Backbone.Collection.extend({
  model: DataSnapshot
});

var DataSnaphots = new DataSnapshotCollection;
var AdditionalDataSnaphots = new DataSnapshotCollection;

// **************************** VIEWS 

var TableView = Backbone.View.extend({
  render: function() {
    return _.template($("#template-table").html())(this.model.toJSON());
  }
});

var DataSnaphotsView = Backbone.View.extend({
  initialize : function(){
 this.activeViews = [
        { id:"People",
          title:"People",
          fields: ["Population","Populationpercentchange","Population in 2000",
                   "Personsunderyearsoldpercent","Personsyearsoldandoverpercent","Femalepersonspercent"]},
        { id:"Demographics", 
          title:"Demographics",
          fields: ["Whitepersonspercent","Blackpersonspercent","AmericanIndianandAlaskaNativepersonspercent","Asianpersonspercent",
                   "NativeHawaiianandOtherPacificIslanderpercent","Personsreportingtwoormoreracespercent","PersonsofHispanicorLatinooriginpercent",
                   "WhitepersonsnotHispanicpersons"]},
        { id:"People origin",
          title:"People origin",
          fields: ["Livinginsamehouseyearagopctyroldover","Foreignbornpersonspercent","LanguageotherthanEnglishspokenathomepctage",
                   "Highschoolgraduatespercentofpersonsage","Bachelorsdegreeorhigherpctofpersonsage","Veterans",
                   "Meantraveltimetoworkminutesworkersage"]},
        { id:"People housing",
          title:"People housing",
          fields: ["Housingunits","Homeownershiprate","Housingunitsinmultiunitstructurespercent","Medianvalueofowneroccupiedhousingunits"]},
        { id:"Household",
          title:"Household", 
          fields: ["Households","Personsperhousehold","Percapitamoneyincomeinpastmonthsdollars","Medianhouseholdincome","Personsbelowpovertylevelpercent"]},
        { id:"Playground",
          title:"Playground", 
          fields: ["Households","Personsperhousehold","Percapitamoneyincomeinpastmonthsdollars","Medianhouseholdincome","Personsbelowpovertylevelpercent"]}];

    this.additionalViews = [
        { id:"Business",
          title:"Business",
          fields: ["Privatenonfarmestablishments","Privatenonfarmemployment","Privatenonfarmemploymentpercentchange","Nonemployerestablishments"]},
        { id:"Business companies",
          title:"Business companies",
          fields: ["Totalnumberoffirms","Blackownedfirmspercent","AmericanIndianandAlaskaNativeownedfirmspercent",
                   "Asianownedfirmspercent","NativeHawaiianandOtherPacificIslanderownedfirmspercent",
                   "Hispanicownedfirmspercent","Womenownedfirmspercent"]},
        { id:"Business types",
          title:"Business types",
          fields: ["Manufacturersshipments","Merchantwholesalersales",
                   "Retailsales","Retailsalespercapita","Accommodationandfoodservicessales",
                   "Buildingpermits","Federalspending"]},                   
        { id:"Geography",
          title:"Geography",
          fields: ["Landarea","Personspersquaremile","FIPSCode"]},
        { id:"Energy sources",
          title:"Energy sources",
          fields: ["TotalEnergy","Coal","NaturalGas","Petroleum","TotalFossilFuel","NuclearElectricPower","RenewableEnergy"]},
        { id:"Energy exchanges",
          title:"Energy exchanges",
          fields: ["NetInterstateFlow","NetElectricityImports"]},
        { id:"Energy usage",
          title:"Energy usage",
          fields: ["EndUseResidential","EndUseCommercial","EndUseIndustrial","EndUseTransportation"]}];        

        this.addView = function(view_object){
            this.activeViews.push(view_object);
            DataSnaphots.reset(this.activeViews);
        },

  	DataSnaphots.bind('add', this.addOne, this);
  	DataSnaphots.bind('reset', this.addAll, this);

        AdditionalDataSnaphots.bind('add', this.addOne, this); 
        AdditionalDataSnaphots.bind('reset', this.addAll, this); 
  	
  	DataSnaphots.reset(this.activeViews);
        AdditionalDataSnaphots.reset(this.additionalViews);
  },	

  addOne : function(){
  	
  }, 	

  addAll : function(){
  	this.render();
  },	

  selectDefaultView : function(){
  	$(".data-view-selector").first().trigger("click");
  },

  render: function() {
  	$("#content_nav").html(_.template($("#template-data-views").html())({views : DataSnaphots.toJSON(), additionalViews : AdditionalDataSnaphots.toJSON()}));
  	
  	$(".data-view-selector").click(_.bind(function(e){	
                $('ul.tabs li.active').removeClass('active'); 
  		$(e.target).parent().parent().children(".active").removeClass("active");
  		$(e.target).parent().addClass("active");
  		
  		this.selectedView = DataSnaphots.get($(e.target).attr("data-view-id"));
                if (!this.selectedView) this.selectedView = AdditionalDataSnaphots.get($(e.target).attr("data-view-id"));                
  		this.trigger("selected-view-changed");
                e.stopPropagation();
  	
  	}, this));
  }
});
