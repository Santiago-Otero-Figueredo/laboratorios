function calendarioTimeLine(eventos=[], acciones=false, editable=false, droppable=false,
    vistaInicial='dayGridMonth', horaMinima='06:00:00', horaMaxima='22:00:00'){

    if(acciones){
        var containerEl = document.getElementById('external-events');
        var Draggable = FullCalendarInteraction.Draggable;
        new Draggable(containerEl, {
        itemSelector: '.fc-event',
        eventData: function(eventEl) {
            return {
            title: eventEl.innerText,
            color: eventEl.getAttribute('data-color')
            };
        }
        });
    }

    // fullcalendar

    var calendarElm = document.getElementById('calendar');
	var calendar = new FullCalendar.Calendar(calendarElm, {
        headerToolbar: {
            left: 'dayGridMonth,timeGridWeek,timeGridDay',
            center: 'title',
            right: 'prev,next today'
        },
        buttonText: {
            today: 'Hoy',
            month: 'Mes',
            week: 'Semana',
            day: 'Día'
        },
        initialView: vistaInicial,
        editable: editable,
        droppable: droppable,
        locale: 'es-us',
        themeSystem: 'bootstrap',
        slotMinTime: horaMinima,
        slotMaxTime: horaMaxima,
        events: eventos
        }
    );
	calendar.render();
};