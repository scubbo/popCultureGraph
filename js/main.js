// CONSTANTS
window.CLICK_DISTANCE = 10;
window.START_NODE_WIDTH = 3;
window.START_EDGE_WIDTH = 1;
window.SELECTION_HIGHLIGHT_TRANSITION_TIME = 0.5
window.SELECTION_HIGHLIGHT_TIME = 2000;

(function($){

  var Renderer = function(canvas){
    var canvas = $(canvas).get(0)
    var ctx = canvas.getContext("2d");
    window.ctx = ctx
    var particleSystem

    var that = {
      init:function(system){
        //
        // the particle system will call the init function once, right before the
        // first frame is to be drawn. it's a good place to set up the canvas and
        // to pass the canvas size to the particle system
        //
        // save a reference to the particle system for use in the .redraw() loop
        particleSystem = system

        // inform the system of the screen dimensions so it can map coords for us.
        // if the canvas is ever resized, screenSize should be called again with
        // the new dimensions
        particleSystem.screenSize(canvas.width, canvas.height) 
        particleSystem.screenPadding(80) // leave an extra 80px of whitespace per side
        
        // set up some event handlers to allow for node-dragging
        that.initMouseHandling()
      },
      
      redraw:function(){
        // 
        // redraw will be called repeatedly during the run whenever the node positions
        // change. the new positions for the nodes can be accessed by looking at the
        // .p attribute of a given node. however the p.x & p.y values are in the coordinates
        // of the particle system rather than the screen. you can either map them to
        // the screen yourself, or use the convenience iterators .eachNode (and .eachEdge)
        // which allow you to step through the actual node objects but also pass an
        // x,y point in the screen's coordinate system
        // 
        ctx.fillStyle = "white"
        ctx.fillRect(0,0, canvas.width, canvas.height)
        
        particleSystem.eachEdge(function(edge, pt1, pt2){
          // edge: {source:Node, target:Node, length:#, data:{}}
          // pt1:  {x:#, y:#}  source position in screen coords
          // pt2:  {x:#, y:#}  target position in screen coords

          // draw a line from pt1 to pt2
          ctx.strokeStyle = edge.data.strokeStyle != undefined ? edge.data.strokeStyle : "rgba(0,0,0, .333)"
          if (edge.data.w != undefined) {
            w = edge.data.w
          } else {
            w = edge.data.originalW
          }
          ctx.lineWidth = w
          ctx.beginPath()
          ctx.moveTo(pt1.x, pt1.y)
          ctx.lineTo(pt2.x, pt2.y)
          ctx.stroke()
          if (edge.data.showName) {
            //Write the name of the edge
            ctx.fillStyle = "gray"
            ctx.fillRect((pt1.x+pt2.x)/2-3, (pt1.y+pt2.y)/2-9, ctx.measureText(edge.data.name).width+6, 12)
            ctx.fillStyle = "white"
            ctx.fillText(edge.data.name,(pt1.x+pt2.x)/2,(pt1.y+pt2.y)/2)
          }
        })

        particleSystem.eachNode(function(node, pt){
          // node: {mass:#, p:{x,y}, name:"", data:{}}
          // pt:   {x:#, y:#}  node position in screen coords

          // draw a circle centered at pt
          if (node.data.w != undefined) {
            w = node.data.w
          } else {
            w = node.data.originalW
          }
          ctx.fillStyle = node.data.color != undefined ? node.data.color : "black"
          ctx.beginPath()
          ctx.arc(pt.x, pt.y, w, 0, 2*Math.PI)
          ctx.fill()
          if (node.data.name != undefined) {
            ctx.strokeStyle = 'rgba(0,0,0,.333)';
            ctx.fillText(node.data.name,pt.x-w/2, pt.y-w/2-10)
          }
        })              
      },
      
      initMouseHandling:function(){
        // no-nonsense drag and drop (thanks springy.js)
        var dragged = null;

        function markNodeSelected(node, truth) {
          node.data.selected = truth;
          width = truth ? node.data.originalW + 10: node.data.originalW
          particleSystem.tweenNode(node, 0.1, {w:width});
          $.each(node.data.edges, function(index,elem) {
            elem.data.showName = truth;
          });
        }

        // set up a handler object that will initially listen for mousedowns then
        // for moves and mouseups while dragging
        var handler = {
          moved:function(e) {
            var pos = $(canvas).offset();
            _mouseP = arbor.Point(e.pageX-pos.left, e.pageY-pos.top)
            nearest = particleSystem.nearest(_mouseP)
            if (!nearest.node) return false

            withinRange = nearest.distance < nearest.node.data.w // This is a HORRIBLE hack and there should be a better way
            markNodeSelected(nearest.node, !!withinRange);
          },
          clicked:function(e){
            var pos = $(canvas).offset();
            _mouseP = arbor.Point(e.pageX-pos.left, e.pageY-pos.top)
            dragged = particleSystem.nearest(_mouseP).distance < window.CLICK_DISTANCE ? particleSystem.nearest(_mouseP) : null
            

            if (dragged && dragged.node !== null){
              // while we're dragging, don't let physics move the node
              dragged.node.fixed = true
              dragged.node.data['color'] = '#000';
              //particleSystem.tweenNode(dragged.node, 0.5, {color:'#000000'})
              //TODO: Bugfix why tweening doesn't work here
            }

            $(canvas).bind('mousemove', handler.dragged)
            $(window).bind('mouseup', handler.dropped)

            return false
          },
          dragged:function(e){
            var pos = $(canvas).offset();
            var s = arbor.Point(e.pageX-pos.left, e.pageY-pos.top)

            if (dragged && dragged.node !== null){
              var p = particleSystem.fromScreen(s)
              dragged.node.p = p
            }

            return false
          },

          dropped:function(e){
            if (dragged===null || dragged.node===undefined) return
            if (dragged.node !== null) {
              dragged.node.fixed = false
              particleSystem.tweenNode(dragged.node, 0.5, {color:dragged.node.data.originalColor})
              //dragged.node.data['color'] = dragged.node.data.originalColor
            }
            dragged.node.tempMass = 1000
            dragged = null
            $(canvas).unbind('mousemove', handler.dragged)
            $(window).unbind('mouseup', handler.dropped)
            $(canvas).bind('mousemove', handler.moved)
            _mouseP = null
            return false
          }
        }
        
        // start listening
        $(canvas).mousedown(handler.clicked);
        $(canvas).bind('mousemove', handler.moved)
      },
      
    }
    return that
  }    

  $(document).ready(function(){
    fillInDropdown('actor');
    fillInDropdown('franchise');

    var sys = arbor.ParticleSystem(1000, 600, 0.5) // create the system with sensible repulsion/stiffness/friction
    window.sys = sys // make global
    sys.parameters({gravity:true}) // use center-gravity to make the graph settle nicely (ymmv)
    sys.renderer = Renderer("#viewport") // our newly created renderer will have its .init() method called shortly by sys...

    $('#submitButton').click(submitButtonAction);
    $('#repulsionUpButton').click(function(){adjustRepulsion(10)});
    $('#repulsionDownButton').click(function(){adjustRepulsion(-10)});

    $('.nameDropdown').change(temporarilyHighlightNode);


    // add some nodes to the graph and watch it go...

    $.post('cgi-bin/getAll.py', function(resp){
      data = resp['data']
      $.each(data, function(index, elem) {
        if (!(sys.getNode('actor_'+elem.actorId))) {
          sys.addNode('actor_'+elem.actorId, {color:'#f00',name:elem.actorName,originalColor:'#f00',originalW:window.START_NODE_WIDTH,edges:[],neighbours:[]})
        }

        if (!(sys.getNode('franchise_'+elem.franchiseId))) {
          sys.addNode('franchise_'+elem.franchiseId, {color:'#00f',name:elem.franchiseName,originalColor:'#00f',originalW:window.START_NODE_WIDTH,edges:[],neighbours:[]})
        }

        edge = sys.addEdge('actor_' + elem.actorId, 'franchise_' + elem.franchiseId, {name:elem.charName,originalW:window.START_EDGE_WIDTH});
        node1 = sys.getNode('actor_' + elem.actorId)
        node2 = sys.getNode('franchise_' + elem.franchiseId)
        node1.data.edges[node1.data.edges.length] = edge
        node2.data.edges[node2.data.edges.length] = edge
        node1.data.neighbours[node1.data.neighbours.length] = node2
        node2.data.neighbours[node2.data.neighbours.length] = node1
      });
    });

  })

})(this.jQuery)

function fillInDropdown(tableName) {
  var dropdown = $('#' + tableName + 'NameDropdown');
  dropdown.append('<option value="0">Please select...</option>');
  $.post('cgi-bin/get.py', {'requestTable':tableName + 's', 'sortByName':'true'}, function(response) {
    $.each(response['data'], function(index, elem) {
      dropdown.append('<option value="' + elem['id'] + '">' + elem['name'] + '</option>');
    });
    dropdown.append('<option value="-1">Add new...</option>');
  });
}

function submitButtonAction() {
  actorNameDropdownValue = $('#actorNameDropdown').val();
  franchiseNameDropdownValue = $('#franchiseNameDropdown').val();
  if (actorNameDropdownValue == 0 || franchiseNameDropdownValue == 0) {
    alert('You need to select an actor and a franchise!');
    return false;
  }

  newCharData = {};
  newCharData['charName'] = $('#charName').val();
  $('#charName').val('');
  if ($('#actorNameDropdown').val() == -1) {
    actorName = $('#actorName').val();
    if (actorName == '') {
      alert('Please enter an Actor\'s name!');
      return false;
    }
    newCharData['actorName'] = actorName;
  } else {
    newCharData['actorId'] = $('#actorNameDropdown').val();
  }
  $('#actorName').val('');
  $('#actorNameDropdown').val(0)

  if ($('#franchiseNameDropdown').val() == -1) {
    newCharData['franchiseName'] = $('#franchiseName').val();
  } else {
    newCharData['franchiseId'] = $('#franchiseNameDropdown').val();
  }
  $('#franchiseName').val('');
  $('#franchiseNameDropdown').val(0);

  $.post('cgi-bin/add.py', newCharData, function(response) {
    console.log(response);
  });

  if (newCharData.franchiseId && newCharData.actorId) {
    franchiseNode = window.sys.getNode('franchise_' + newCharData.franchiseId)
    actorNode = window.sys.getNode('actor_' + newCharData.actorId)
    if (franchiseNode && actorNode) {
      edge = window.sys.addEdge('franchise_' + newCharData.franchiseId, 'actor_' + newCharData.actorId, {})
      franchiseNode.data.edges[franchiseNode.data.edges.length] = edge
      actorNode.data.edges[actorNode.data.edges.length] = edge
    }
  }

}

function adjustRepulsion(value) {
  var initialParams = window.sys.parameters();
  initialParams.repulsion += value;
  window.sys.parameters(initialParams);
  $('#repulsionValue').html(initialParams.repulsion.toString())
}

function temporarilyHighlightNode(e) {
  target = $(e.currentTarget)
  targetId = target[0].id
  nodeToHighlight = targetId.replace('NameDropdown','') + '_' + target.val()

  node = window.sys.getNode(nodeToHighlight)
  mainNodePreHighlightWidth = parseInt(node.data.w != undefined ? node.data.w : node.data.originalW)
  mainNodePostHighlightWidth = parseInt(mainNodePreHighlightWidth) + 10
  window.sys.tweenNode(node, window.SELECTION_HIGHLIGHT_TRANSITION_TIME, {w:mainNodePostHighlightWidth});
  setTimeout(function() {
    window.sys.tweenNode(node, window.SELECTION_HIGHLIGHT_TRANSITION_TIME, {w:mainNodePreHighlightWidth})
  }, window.SELECTION_HIGHLIGHT_TIME)

  edgesFrom = window.sys.getEdgesFrom(node)
  $.each(edgesFrom, function(index, elem) {
    fromEdgePreHighlightWidth = parseInt(elem.data.w != undefined ? elem.data.w : elem.data.originalW)
    elem.data.showName = true
    window.sys.tweenEdge(elem, window.SELECTION_HIGHLIGHT_TRANSITION_TIME, {w:fromEdgePreHighlightWidth+3})
    setTimeout(function() {
      elem.data.showName = false
      window.sys.tweenEdge(elem, window.SELECTION_HIGHLIGHT_TRANSITION_TIME, {w:fromEdgePreHighlightWidth})
    }, window.SELECTION_HIGHLIGHT_TIME)

    var targetNode = elem.target
    var preHighlightNodeWidth = parseInt(targetNode.data.w != undefined ? targetNode.data.w : targetNode.data.originalW)
    window.sys.tweenNode(targetNode, window.SELECTION_HIGHLIGHT_TRANSITION_TIME, {w:preHighlightNodeWidth+5})
    setTimeout(function() {
      window.sys.tweenNode(targetNode, window.SELECTION_HIGHLIGHT_TRANSITION_TIME, {w:preHighlightNodeWidth})
    }, window.SELECTION_HIGHLIGHT_TIME)
  })

  edgesTo = window.sys.getEdgesTo(node)
  $.each(edgesTo, function(index, elem) {
    var preHighlightWidth = parseInt(elem.data.w != undefined ? elem.data.w : elem.data.originalW)
    elem.data.showName = true
    window.sys.tweenEdge(elem, window.SELECTION_HIGHLIGHT_TRANSITION_TIME, {w:preHighlightWidth+3})
    setTimeout(function() {
      elem.data.showName = false
      window.sys.tweenEdge(elem, window.SELECTION_HIGHLIGHT_TRANSITION_TIME, {w:preHighlightWidth})
    }, window.SELECTION_HIGHLIGHT_TIME)

    var sourceNode = elem.source
    var preHighlightNodeWidth = parseInt(sourceNode.data.w != undefined ? sourceNode.data.w : sourceNode.data.originalW)
    window.sys.tweenNode(sourceNode, window.SELECTION_HIGHLIGHT_TRANSITION_TIME, {w:preHighlightNodeWidth+5})
    setTimeout(function() {
      window.sys.tweenNode(sourceNode, window.SELECTION_HIGHLIGHT_TRANSITION_TIME, {w:preHighlightNodeWidth})
    }, window.SELECTION_HIGHLIGHT_TIME)

  })

}
