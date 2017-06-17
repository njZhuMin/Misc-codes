// ==UserScript==
// @name         Zhihu Shortcuts
// @author       SilverLining
// @description  Restore shortcuts feature for zhihu new webpage
// @match        *://www.zhihu.com/question/*
// ==/UserScript==

(function() {
    'use strict';
    var selectId=0;
    var gFlag = 0, scFlag = 0, fxFlag = 0;
    // add hotkey
    document.onkeydown = hotkey;
    var lists = document.getElementsByClassName('ContentItem AnswerItem');
    var list = document.getElementsByClassName('List')[0];
    list.addEventListener('click',showColor,true);
    list.addEventListener('DOMNodeInserted', addEventId, true);

    function showColor(e){
      var element = e.target;
      selectId = parents(element);
    }
    function parents(element){
      var parent = element.parentNode;
      if(parent.className != 'ContentItem AnswerItem'){
        return parents(parent);
      }
      return parent.parentNode.getAttribute('count');
    }
    // add id
    function addEventId() {
      for (var i=0; i<lists.length; i++){
        var id = lists[i].getAttribute('name');
        lists[i].parentNode.setAttribute('count', i);
        lists[i].parentNode.setAttribute('id', id);
      }
    }

    function findId(count) {
      return lists[count].getAttribute('name');
    }
    function findAnswers(count) {
      return lists[count];
    }
    function nextItem() {
      var length = lists.length-1;
      if(selectId != length){
        selectId++;
      }
      location.hash="";
      location.hash=findId(selectId);
    }
    function previousItem() {
      if(selectId !== 0){
        selectId--;
      }
      location.hash="";
      location.hash=findId(selectId);
    }
    function voteButtonUp() {
      var answers = findAnswers(selectId);
      var voteButton = answers.getElementsByClassName('VoteButton--up')[0];
      voteButton.click();
    }
    function voteButtonDown() {
      var answers = findAnswers(selectId);
      var voteButton = answers.getElementsByClassName('VoteButton--down')[0];
      voteButton.click();
    }
    function search()
    {
      var searchInput = document.getElementsByClassName('SearchBar-input')[0];
      searchInput.focus();
    }
    function openComment()
    {
      var answers = findAnswers(selectId);
      var comment = answers.getElementsByClassName('ContentItem-actions')[0].childNodes[1];
      comment.click();
    }
    function thank()
    {
      var answers = findAnswers(selectId);
      var thinkButton = answers.getElementsByClassName('ContentItem-actions')[0].childNodes[4];
      thinkButton.click();
    }
    function firstItem()
    {
      gFlag++;
      if(gFlag == 2){
        gFlag = 0;
        selectId = 0;
        location.hash=findId(selectId);
      }
    }
    function lastItem(){
      selectId = lists.length - 1;
      location.hash=findId(selectId);
    }
    function collection()
    {
      var answers = findAnswers(selectId);
      var thinkButton = answers.getElementsByClassName('ContentItem-actions')[0].childNodes[3];
      thinkButton.click();
    }
    function share()
    {
      var answers = findAnswers(selectId);
      var share = answers.getElementsByClassName('ContentItem-actions')[0].childNodes[2];
      var button = share.getElementsByTagName('button')[0];
      button.click();
    }
    function hotkey()
    {
      if(window.event.key=='s') {
        scFlag = 1;
      } else if(window.event.key=='f') {
        fxFlag = 1;
      } else if(scFlag == 1 && window.event.key=='c') {
        collection();
        scFlag = fxFlag = 0;
        return;
      } else if(fxFlag == 1 && window.event.key=='x') {
        share();
        scFlag = fxFlag = 0;
        return;
      }
      else {
        scFlag = fxFlag = 0;
      }

      switch (window.event.key) {
        case 'j':
          nextItem();
          break;
        case 'k':
          previousItem();
          break;
        case '/':
          search();
          break;
        case '?':
          break;
        case 'g':
          firstItem();
          break;
        case 'o':
          break;
        case 'c':
          openComment();
          break;
        case 'v':
          voteButtonUp();
          break;
        case 'd':
          voteButtonDown();
          break;
        case 't':
          thank();
          break;
        default:

      }
    }
})();
