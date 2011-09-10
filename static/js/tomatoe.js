
var Query = Backbone.Model.extend({
	
	/*
	 * 	{
	 * 	
	 * 		states : [],	
	 * 		fields : []
	 * }
	*/
	
	addState : function(state){
		var currentStates = this.get("states");
		if(undefined == currentStates) currentStates = [];
		
		currentStates.push(state);
		this.set({states : currentStates});
	},
	
	removeState : function(state){
		var currentStates = this.get("states");
		if(undefined == currentStates) currentStates = [];
		
		currentStates = _.reject(currentStates, function(s){ return s == state; }); 
		this.set({states : currentStates});
	},
	
	addField : function(field){
		var currentFields = this.get("fields");
		if(undefined == currentFields) currentFields = [];
		
		currentFields.push(field);
		this.set({fields : currentFields});
	},
	
	removeField : function(field){
		var currentFields = this.get("fields");
		if(undefined == currentFields) currentFields = [];
		
		currentFields = _.reject(currentFields, function(s){ return s == field; }); 
		this.set({fields : currentFields});
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
 		  	return "/data?" + this.get("query");
 		  }	
	},
	{
		
	}

);

var fixture = new Dataset;
fixture.set(
	{ 
		
		query : "states=al,ca,wi&fields=f1,f2,f3",
		
		columns : [ {title:"Col1", desc:"column 1"}, 
					{title:"Col2", desc:"column 2"}, 
					{title:"Col3", desc:"column 1"} ],
					
		data : [ [1,2,3], [4,5,6], [7,8,9] ] 
	}
	
);

var TableView = Backbone.View.extend({

  render: function() {
    return _.template($("#template-table").html())(this.model.toJSON());
  }

});