# coding=utf-8
from PySide.QtCore import *
from PySide.QtGui import *
import sqlalchemy as sql
import sqlalchemy.orm as orm
import sys
from views.ui_database_settings import Ui_Dialog
from delegates.mainwindow import tournament_delegate
from views.ui_mainwindow import Ui_MainWindow
import settings
#import logging

#logging.basicConfig()
#logging.getLogger('sqlalchemy.engine').setLevel(logging.INFO)

__author__ = 'anton'


class TournamentItem(QStandardItem):
    def __init__(self, item, *args, **kwargs):
        super(TournamentItem, self).__init__(*args, **kwargs)
        self.item = item
        self.setData(u'%s %s %s' % (item.id, item.title, item.added), Qt.DisplayRole)


class TournamentListModel(QStandardItemModel):
    def __init__(self, *args, **kwargs):
        super(TournamentListModel, self).__init__(*args, **kwargs)


class empty: pass


class RegistrationMode:
    Pair = 0
    Solo = 1
    Duet = 2
    Group = 3
    Trio = 4
    Formation = 5


SOURCE_TABLES = [
    'tournament', 'dancer', 'age', 'chief', 'city', 'ligue', 'registration_title',
    'dancer_ligue', 'ligue_discipline',
    'club', 'country', 'discipline', 'nomination', 'person', 'profile',
    'profiles_field', 'region', 'subscribe', 'tournament_rank',
    'registration', 'tournament_rank_rule', 'trainer', 'trainer_dancer', 'user',
    'tournament_day',
]
for table in SOURCE_TABLES:
    exec ('class src%s(object):pass' % table.title())

TARGET_TABLES = [
    'dancerorgprgclasses', 'couples', 'dancers', 'categorystate', 'cities', 'clubs',
    'countries', 'dances', 'programdances', 'registration', 'dancerclasses', 'membershiptypes',
    'organisations', 'programs', 'trainers', 'viddils', 'viddilsdata', 'categories',
    'categoryprograms', 'competitions', 'danceprogram', 'disqualifications', 'payments',
    'trainercategories', 'updates', 'winners', 'zahody',
]
for table in TARGET_TABLES:
    exec ('class tar%s(object):pass' % table.title())

TARGET2_TABLES = [
    'categorystate', 'dances', 'programdances', 'registration',
    'programs', 'viddils', 'viddilsdata', 'categories',
    'categoryprograms', 'danceprogram', 'disqualifications', 'winners', 'zahody',
    'judges', 'judgeprogram', 'judgegroups', 'judgegroupmembers', 'marks', 'redance',
]
for table in TARGET2_TABLES:
    exec ('class tar2%s(object):pass' % table.title())


class database_settings(QDialog):
    def __init__(self, *args, **kwargs):
        super(database_settings, self).__init__(*args, **kwargs)
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)


class mainwindow(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        settings = database_settings()
        settings.closeEvent = self.exit
        ok = False
        while not ok:
            if settings.exec_():
                ok, error_message = self.check_connection(settings)
                if not ok:
                    QMessageBox.warning(self, u'Ошибка входа',
                                        u"<p>Ошибка подключения к базе данных.<br/>Проверьте ещё раз параметры подключения</p><b>%s</b>" % error_message)
            else:
                self.exit()
        self.initialize()

    def check_connection(self, form):
        settings.TARGET_SERVER = form.ui.txtServer.text()
        settings.TARGET_PORT = form.ui.txtPort.text()
        settings.TARGET_USER = form.ui.txtLogin.text()
        settings.TARGET_PASSWORD = form.ui.txtPassword.text()
        try:
            test = sql.create_engine("mysql+mysqldb://%s:%s@%s:%s/%s?charset=utf8" % (
                settings.TARGET_USER, settings.TARGET_PASSWORD, settings.TARGET_SERVER, settings.TARGET_PORT,
                settings.TARGET_DB))
            test.begin()
            return True, None
        except Exception, e:
            return False, e.message

    def exit(self, arg=None):
        sys.exit(0)

    def initialize(self, arg=None):
        self.ui.list_tournaments.setItemDelegate(tournament_delegate(self))
        self.tournaments = TournamentListModel()
        self.ui.list_tournaments.setModel(self.tournaments)

        self.ui.list_tournaments.selectionChanged = self.on_list_tournaments_selectionChanged

        self.configure_db()
        self.load_tournaments()
        self.ui.list_tournaments.setCurrentIndex(self.tournaments.index(0, 0))
        self.ui.list_tournaments.setFocus()

    def configure_db(self):
        self.source = sql.create_engine("mysql+mysqldb://%s:%s@%s:%s/%s?charset=utf8" % (
            settings.SOURCE_USER, settings.SOURCE_PASSWORD, settings.SOURCE_SERVER, settings.SOURCE_PORT,
            settings.SOURCE_DB))
        self.source.echo = True
        self.db = empty()
        self.source.metadata = sql.MetaData(self.source)

        for table in SOURCE_TABLES:
            try:
                exec ("self.db.%s = sql.Table('%s', self.source.metadata, autoload=True)" % (table, table))
                exec ("orm.mapper(src%s, self.db.%s)" % (table.title(), table))
            except Exception, e:
                print 'Error while loading table <%s>' % table
                raise e

        self.target = sql.create_engine("mysql+mysqldb://%s:%s@%s:%s/%s?charset=cp1251" % (
            settings.TARGET_USER, settings.TARGET_PASSWORD, settings.TARGET_SERVER, settings.TARGET_PORT,
            settings.TARGET_DB))
        self.target.echo = False
        self.target.metadata = sql.MetaData(self.target)

        try:
            self.target.execute("ALTER TABLE `couples` ADD INDEX `CoupleIndex` (`CoupleIndex`)")
        except Exception, e:
            print str(e)

        for table in TARGET_TABLES:
            exec (
                "self.db.%s = sql.Table('%s', self.target.metadata, autoload=True, mysql_engine='MyISAM')" % (
                    table, table))
            exec ("orm.mapper(tar%s, self.db.%s)" % (table.title(), table))

        self.session = orm.create_session()

    def configure_db2(self, competitionid):
        self.target2 = sql.create_engine("mysql+mysqldb://%s:%s@%s:%s/dancecompetition%s?charset=cp1251" % (
            settings.TARGET_USER, settings.TARGET_PASSWORD, settings.TARGET_SERVER, settings.TARGET_PORT,
            competitionid))
        self.target2.echo = False
        self.target2.metadata = sql.MetaData(self.target2)

        for table in TARGET2_TABLES:
            exec (
                "self.db.%s2 = sql.Table('%s', self.target2.metadata, autoload=True, mysql_engine='MyISAM')" % (
                    table, table))
            exec ("orm.mapper(tar2%s, self.db.%s2)" % (table.title(), table))

        self.session.close()
        self.session = orm.create_session()
        self.session.autocommit = True
        self.session.autoflush = True

    def load_tournaments(self):
        root = self.tournaments.invisibleRootItem()
        for tournament in self.session.query(srcTournament):
            root.appendRow(TournamentItem(tournament))

    def on_list_tournaments_selectionChanged(self, selection, args):
        selected = selection.indexes()[0]
        item = self.tournaments.itemFromIndex(selected).item
        self.dancers = QStandardItemModel()
        self.ui.list_dancers.setModel(self.dancers)
        root = self.dancers.invisibleRootItem()
        for registration, dancer, person, nomination, discipline in \
            self.session.query(srcRegistration, srcDancer, srcPerson, srcNomination, srcDiscipline) \
                .filter(srcRegistration.tournament_id == item.id) \
                .filter(srcRegistration.dancer_id == srcDancer.id) \
                .filter(srcRegistration.nomination_id == srcNomination.id) \
                .filter(srcRegistration.discipline_id == srcDiscipline.id) \
                .filter(srcDancer.person_id == srcPerson.id) \
                .limit(200):
            root.appendRow(QStandardItem('%s %s %s - %s, %s' % (
                registration.number, person.surname, person.name, nomination.title, discipline.title)))

    @Slot()
    def on_cmdImport_clicked(self):
        indexes = self.ui.list_tournaments.selectedIndexes()
        day = int(self.ui.cmbDay.currentText())
        if not indexes:
            QMessageBox.information(self, u'Information', u"Выбирите турнир")
            return
        tournament = self.tournaments.itemFromIndex(indexes[0]).item
        if QMessageBox.question(self, "Question",
                                u"Вы хотите импортировать регистрацию на турнир \"%s\",\nдобавленный %s" %
                                        (tournament.title, tournament.added), QMessageBox.Yes | QMessageBox.No,
                                QMessageBox.No) == QMessageBox.No:
            return
        self.start_import(tournament, day)

    def create_target2_db(self, id):
        import os, shutil

        path = "c:\\mysql\\data\\dancecompetition%s" % id
        os.mkdir(path)
        for filename in os.listdir('dancecompetition'):
            source = os.path.abspath(os.path.join('dancecompetition', filename))
            target = os.path.join(path, filename)
            shutil.copy(source, target)

    @Slot()
    def tournament_selected(self):
        pass

    def start_import(self, tournament, day):
        items = []
        f = open("file.log", "w")
        f.truncate()
        def add(item):
            self.session.add(item)
            items.append(item)
            self.session.begin()
            self.session.commit()

        progress = QProgressDialog("Importing...", "Wait", 0, 100, self)
        progress.setMinimumWidth(600)
        progress.show()
        self.session.autocommit = True
        self.session.autoflush = True
        try:
            competition = self.session.query(tarCompetitions).filter(tarCompetitions.Name == tournament.title).first()
            if not competition:
                competition = tarCompetitions()
                competition.Name = tournament.title
                competition.DateFrom = tournament.registration_start
                competition.DateTo = tournament.tournament_end
                competition.RegistrationEndDate = tournament.registration_end
                add(competition)
                self.create_target2_db(competition.CompetitionIndex)
            self.configure_db2(competition.CompetitionIndex)

            #registrations
            rs = {}

            class RegistrationEntry:
                def __init__(self, registration, dancer, person, nomination, discipline, club):
                    self.registration = registration
                    self.dancer = dancer
                    self.person = person
                    self.nomination = nomination
                    self.discipline = discipline
                    self.club = club

            def next_couple_index():
                item = self.session.query(sql.func.max(tarCouples.CoupleIndex)).first()
                if item and len(item) > 0 and item[0]:
                    return item[0] + 1
                return 1

            def next_categoryprogram_index():
                item = self.session.query(sql.func.max(tar2Categoryprograms.CategoryProgramNumber)).first()
                if item and len(item) > 0 and item[0]:
                    return item[0] + 1
                return 1

            QApplication.processEvents()
            ##########################################################################################################
            # Creating all categories, programs and categoryprograms
            all_items = self.session.query(srcDiscipline) \
                        .filter(srcTournament_Day.discipline_id == srcDiscipline.id) \
                        .filter(srcTournament_Day.day == day) \
                        .distinct() \
                        .count()
            done = 0
            rank_n = 1
            for discipline in self.session.query(srcDiscipline) \
                                .filter(srcTournament_Day.discipline_id == srcDiscipline.id) \
                                .filter(srcTournament_Day.day == day) \
                                .order_by(srcDiscipline.title) \
                                .distinct():
                done += 1

                program = self.session.query(tar2Programs).filter(tar2Programs.ProgramName == discipline.title_short.replace('/', '_')).first()
                if not program:
                    program = tar2Programs()
                    program.ProgramName = discipline.title_short.replace('/', '_')
                    add(program)

                dance = tar2Dances()
                dance.DanceAbbreviation = discipline.abbreviation
                dance.DanceName = discipline.title_short.replace('/', '_')
                dance.DanceNumber = done
                add(dance)

                programdance = tar2Programdances()
                programdance.ProgramRef = program.ProgramIndex
                programdance.DanceRef = dance.DanceIndex
                add(programdance)

                progress.setLabelText(u"Создание категорий для програмы %s" % program.ProgramName)
                progress.setValue(100 * done / all_items)
                QApplication.processEvents()

                ranks = self.session.query(srcTournament_Rank) \
                    .filter(srcTournament_Rank.id == srcRegistration.tournament_rank_id) \
                    .filter(srcRegistration.discipline_id == discipline.id) \
                    .filter(srcRegistration.receipt_id > 0) \
                    .filter(srcTournament_Day.day == day) \
                    .filter(srcRegistration.discipline_id == srcTournament_Day.discipline_id and srcRegistration.nomination_id == srcTournament_Day.nomination_id and srcRegistration.age_id == srcTournament_Day.age_id and srcRegistration.tournament_rank_id == srcTournament_Day.tournament_rank_id and srcRegistration.tournament_id == srcTournament_Day.tournament_id) \
                    .order_by(srcTournament_Rank.title) \
                    .distinct()
                for rank in ranks:

                    viddil = tar2Viddils()
                    viddil.ViddilNumber = rank_n
                    viddil.ViddilName = '%s %s' % (discipline.title_short.replace('/', '_'), rank.title_short.replace('/', '_'))
                    add(viddil)
                    rank_n += 1

                    for nomination, age in \
                        self.session.query(srcNomination, srcAge) \
                        .filter(srcRegistration.age_id == srcAge.id) \
                        .filter(srcRegistration.discipline_id == discipline.id) \
                        .filter(srcRegistration.nomination_id == srcNomination.id) \
                        .filter(srcRegistration.tournament_rank_id == rank.id) \
                        .filter(srcRegistration.receipt_id > 0) \
                        .filter(srcTournament_Day.day == day) \
                        .filter(srcRegistration.discipline_id == srcTournament_Day.discipline_id and srcRegistration.nomination_id == srcTournament_Day.nomination_id and srcRegistration.age_id == srcTournament_Day.age_id and srcRegistration.tournament_rank_id == srcTournament_Day.tournament_rank_id and srcRegistration.tournament_id == srcTournament_Day.tournament_id) \
                        .order_by(srcAge.years_from) \
                        .order_by(srcNomination.title) \
                        .distinct():
                        QApplication.processEvents()

                        category_name = '%s %s %s' % (age.title, nomination.title_short.replace('/', '_'), rank.title_short.replace('/', '_'))
                        category_name = category_name.replace('/', '_')

                        category = tar2Categories()
                        category.CategoryName = category_name
                        category.RegistrationMode = nomination.prog_id
                        category.CalculationMode = '{8965D463-2B8A-4A62-BA52-5F1E9AA61FCF}'
                        add(category)

                        categoryprogram = tar2Categoryprograms()
                        categoryprogram.CategoryRef = category.CategoryIndex
                        categoryprogram.ProgramRef = program.ProgramIndex
                        categoryprogram.CategoryProgramNumber = next_categoryprogram_index()
                        add(categoryprogram)

                        vdata = tar2Viddilsdata()
                        vdata.ViddilRef = viddil.ViddilIndex
                        vdata.CategoryRef = category.CategoryIndex
                        vdata.ProgramRef = program.ProgramIndex
                        add(vdata)
            progress.setLabelText(u"Импорт регистрации")
            all_items = self.session.query(srcRegistration) \
                            .filter(srcRegistration.receipt_id > 0) \
                            .filter(srcTournament_Day.day == day) \
                            .filter(srcRegistration.discipline_id == srcTournament_Day.discipline_id) \
                            .filter(srcRegistration.nomination_id == srcTournament_Day.nomination_id) \
                            .filter(srcRegistration.age_id == srcTournament_Day.age_id) \
                            .filter(srcRegistration.tournament_rank_id == srcTournament_Day.tournament_rank_id) \
                            .filter(srcRegistration.tournament_id == srcTournament_Day.tournament_id) \
                            .count()
            f.write("Total items: " + str(all_items) + "\n");

            done = 0
            numbersDone = set()
            for registration, dancer, person, nomination, discipline, club, city, country, age, rank in \
                self.session.query(srcRegistration, srcDancer, srcPerson, srcNomination, srcDiscipline, srcClub,
                                   srcCity, srcCountry, srcAge, srcTournament_Rank) \
                    .filter(srcRegistration.tournament_id == tournament.id) \
                    .filter(srcRegistration.dancer_id == srcDancer.id) \
                    .filter(srcRegistration.nomination_id == srcNomination.id) \
                    .filter(srcRegistration.discipline_id == srcDiscipline.id) \
                    .filter(srcRegistration.tournament_rank_id == srcTournament_Rank.id) \
                    .filter(srcDancer.club_id == srcClub.id) \
                    .filter(srcPerson.city_id == srcCity.id) \
                    .filter(srcCity.country_id == srcCountry.id) \
                    .filter(srcAge.id == srcRegistration.age_id) \
                    .filter(srcDancer.person_id == srcPerson.id) \
                    .filter(srcRegistration.receipt_id > 0) \
                    .filter(srcTournament_Day.day == day) \
                    .filter(srcRegistration.discipline_id == srcTournament_Day.discipline_id) \
                    .filter(srcRegistration.nomination_id == srcTournament_Day.nomination_id) \
                    .filter(srcRegistration.age_id == srcTournament_Day.age_id) \
                    .filter(srcRegistration.tournament_rank_id == srcTournament_Day.tournament_rank_id) \
                    .filter(srcRegistration.tournament_id == srcTournament_Day.tournament_id):
                entry = RegistrationEntry(registration, dancer, person, nomination, discipline, club)

                f.write("\n\n")
                f.write("Обработка номера: " + str(registration.number) + '\n')

                f.write("К-во танцоров: " + str(nomination.max_dancer_count) + '\n')

                if nomination.max_dancer_count > 2:
                    arrList = self.session.query(srcRegistration, srcDancer, srcPerson, srcClub, srcCity) \
                        .filter(srcRegistration.dancer_id == srcDancer.id) \
                        .filter(srcDancer.club_id == srcClub.id) \
                        .filter(srcPerson.city_id == srcCity.id) \
                        .filter(srcDancer.person_id == srcPerson.id) \
                        .filter(srcRegistration.receipt_id > 0) \
                        .filter(srcTournament_Day.day == day) \
                        .filter(srcRegistration.discipline_id == srcTournament_Day.discipline_id and srcRegistration.nomination_id == srcTournament_Day.nomination_id and srcRegistration.age_id == srcTournament_Day.age_id and srcRegistration.tournament_rank_id == srcTournament_Day.tournament_rank_id and srcRegistration.tournament_id == srcTournament_Day.tournament_id) \
                        .filter(srcRegistration.number == registration.number) \
                        .group_by(srcClub.id) \
                        .order_by('count(club.id ) desc') \
                        .limit(1)

                    complex = {'fio' : '', 'club': '', 'city' : ''}
                    (oneRegistration, oneDancer, onePerson, oneClub, oneCity) = arrList[0]
                    complex['fio'] = "%s %s %s" % (oneClub.title, oneCity.name, oneRegistration.number)
                    complex['club'] = oneClub.title
                    complex['city'] = oneCity.name
                else:
                    complex = {'fio' : "%s %s" % (person.surname, person.name), 'club': club.title, 'city': city.name}

                progress.setValue(100 * done / all_items)
                QApplication.processEvents()
                done += 1

                program = self.session.query(tar2Programs).filter(tar2Programs.ProgramName == discipline.title_short.replace('/', '_')).first()
                if not program:
                    program = tar2Programs()
                    program.ProgramName = discipline.title_short.replace('/', '_')
                    add(program)
                entry.tarProgram = program

                viddilName = ('%s %s' % (discipline.title_short.replace('/', '_'), rank.title_short.replace('/', '_')))[:50]
                viddil = self.session.query(tar2Viddils).filter(tar2Viddils.ViddilName == viddilName).first()

                category_name = '%s %s %s' % (age.title, nomination.title_short.replace('/', '_'), rank.title_short.replace('/', '_'))
                category_name = category_name.replace('/', '_')

                #checking category and create one if it doesn't exists yet
                #comparison - by name
                category = self.session.query(tar2Categories) \
                    .filter(tar2Categories.CategoryName == category_name) \
                    .filter(tar2Categories.CategoryIndex == tar2Viddilsdata.CategoryRef) \
                    .filter(tar2Viddilsdata.ViddilRef == viddil.ViddilIndex) \
                    .filter(tar2Viddilsdata.ProgramRef == program.ProgramIndex) \
                    .first()
                if not category:
                    f.write('Категория: ')
                    f.write(unicode(category_name).encode('utf8'))
                    f.write('\n')
                    continue



                f.write("Мод регистрации: " + str(category.RegistrationMode) + '\n')

                if not category.RegistrationMode in [RegistrationMode.Pair, RegistrationMode.Duet]:
                    if registration.number in numbersDone:
                        continue
                    numbersDone.add(registration.number)

                f.write("Готовые номера: " + str(numbersDone) + '\n')

                entry.tarCategory = category

                countryName = country.name[:50]
                tarCountry = self.session.query(tarCountries).filter(tarCountries.CountryName == countryName).first()
                if not tarCountry:
                    tarCountry = tarCountries()
                    tarCountry.CountryName = countryName
                    add(tarCountry)

                cityName = complex['city'][:50]
                tarCity = self.session.query(tarCities).filter(tarCities.CityName == cityName).first()
                if not tarCity:
                    tarCity = tarCities()
                    tarCity.CountryRef = tarCountry.CountryIndex
                    tarCity.CityName = cityName
                    add(tarCity)

                clubtitle = complex['club'][:50]
                tarClub = self.session.query(tarClubs) \
                    .filter(tarClubs.ClubName == clubtitle) \
                    .filter(tarClubs.CityRef == tarCity.CityIndex) \
                    .first()
                if not tarClub:
                    tarClub = tarClubs()
                    tarClub.ClubName = clubtitle
                    tarClub.CityRef = tarCity.CityIndex
                    try:
                        add(tarClub)
                    except Exception, eee:
                        tarClub = self.session.query(tarClubs) \
                            .filter(tarClubs.ClubName == clubtitle) \
                            .filter(tarClubs.CityRef == tarCity.CityIndex) \
                            .first()
                        QMessageBox.information(self, '', 'error while creating club (%s:::%s): %s \n\n\n %s' % (
                            clubtitle, tarCity.CityIndex, str(eee), str(tarClub)))

                #checking dancer and create one if neccesary
                fio = "%s %s" % (person.surname, person.name)
                fio = complex['fio']
                d = self.session.query(tarDancers).filter(fio == tarDancers.DancerName).first()
                #undone                    .filter(tarDancers.Birthday == person.birthday) \
                if not d:
                    _chief = self.session.query(srcPerson) \
                        .filter(srcPerson.id == srcChief.person_id) \
                        .filter(srcChief.id == srcClub.chief_id) \
                        .filter(club.id == srcClub.id) \
                        .first()
                    chief = self.session.query(tarTrainers) \
                        .filter(tarTrainers.CityRef == tarCity.CityIndex) \
                        .filter(tarTrainers.ClubRef == tarClub.ClubIndex) \
                        .filter(tarTrainers.TrainerName == '%s %s' % (_chief.surname, _chief.name)) \
                        .first()
                    if not chief:
                        chief = tarTrainers()
                        chief.TrainerName = '%s %s' % (_chief.surname, _chief.name)
                        chief.CityRef = tarCity.CityIndex
                        chief.ClubRef = tarClub.ClubIndex
                        add(chief)

                    trainer_name = ', '.join(['%s %s' % (t.surname, t.name) for t in self.session.query(srcPerson) \
                        .filter(srcTrainer.id == srcTrainer_Dancer.trainer_id) \
                        .filter(srcTrainer.person_id == srcPerson.id) \
                        .filter(srcTrainer_Dancer.discipline_id == discipline.id) \
                        .filter(srcTrainer_Dancer.age_id == age.id) \
                        .filter(srcTrainer_Dancer.nomination_id == nomination.id)]) \
                        or chief.TrainerName

                    trainer = self.session.query(tarTrainers) \
                        .filter(tarTrainers.CityRef == tarCity.CityIndex) \
                        .filter(tarTrainers.ClubRef == tarClub.ClubIndex) \
                        .filter(tarTrainers.TrainerName == trainer_name[:50]) \
                        .first()
                    if not trainer:
                        trainer = tarTrainers()
                        trainer.TrainerName = trainer_name
                        trainer.CityRef = tarCity.CityIndex
                        trainer.ClubRef = tarClub.ClubIndex
                        add(trainer)


                    d = tarDancers()
                    d.DancerName = fio
                    #undone                    d.BirthDay = person.birthday
                    d.TrainerRef = trainer.TrainerIndex if trainer is not None else 0
                    d.ChiefRef = chief.TrainerIndex
                    d.sex = 1 if person.sex == "male" else 0
                    add(d)
                d.ClubRef = tarClub.ClubIndex
                entry.tarDancer = d

                if category.RegistrationMode in [RegistrationMode.Pair, RegistrationMode.Duet]:
                    #adding pair for the latter registration
                    key = (registration.number, registration.nomination_id)
                    if key not in rs:
                        rs[key] = []
                    rs[key].append(entry)
                else:
                    couple = self.session.query(tarCouples).filter(tarCouples.DancerRef == d.DancerIndex) \
                        .filter(tarCouples.GirlRef == 0).first()
                    if not couple:
                        couple = tarCouples()
                        couple.DancerRef = d.DancerIndex
                        couple.CoupleIndex = next_couple_index()
                        add(couple)

                    r = self.session.query(tar2Registration) \
                        .filter(tar2Registration.CategoryRef == category.CategoryIndex) \
                        .filter(tar2Registration.CoupleRef == couple.CoupleIndex) \
                        .filter(tar2Registration.Number == registration.number).first()
                    if not r:
                    #     print 'registration not found. Creating...'
                        compositionName = self.session.query(srcRegistration_Title) \
                            .filter(srcRegistration_Title.number == registration.number).first()
                        r = tar2Registration()
                        r.CoupleRef = couple.CoupleIndex
                        r.CategoryRef = category.CategoryIndex
                        r.Number = registration.number
                        r.CompositionName = compositionName.title if compositionName else ''
                        r.Registered = 1
                        r.RegTrainerRef = d.TrainerRef
                        r.RegChiefRef = d.ChiefRef
                        r.PaidEntry = 0.0
                        r.ProgramRefs = '.%s.' % program.ProgramIndex
                        add(r)
                        print 'registration created: %s, %s, %s, %s' % (
                            r.CoupleRef, r.CategoryRef, r.Number, r.ProgramRefs)
                    else:
                        if '.%s.' % program.ProgramIndex not in r.ProgramRefs:
                            r.ProgramRefs = '%s.%s.' % (r.ProgramRefs, program.ProgramIndex)
                            print 'registration added: %s' % r.ProgramRefs

            print 'Registering pairs/couples: %s' % len(rs)
            progress.setLabelText(u"Registering pairs/couples: %s" % len(rs))

            f.write(unicode(rs) + '\n')

            for key in rs:
                number, nomination_id = key
                programs = set()
                dancers = set()
                for entry in rs[key]:
                    programs.add(entry.tarProgram.ProgramIndex)
                    dancers.add((entry.tarDancer.DancerIndex, entry.tarDancer.Sex,))
                if len(dancers) < 2:
                    continue

                dancers = list(dancers)
                programs = list(programs)
                #first is female1
                if dancers[0][1] == 0:
                    maleid = dancers[1][0]
                    femaleid = dancers[0][0]
                else:
                    maleid = dancers[0][0]
                    femaleid = dancers[1][0]

                couple = self.session.query(tarCouples).filter(tarCouples.DancerRef == maleid) \
                    .filter(tarCouples.GirlRef == femaleid).first()
                if not couple:
                    couple = tarCouples()
                    couple.DancerRef = maleid
                    couple.GirlRef = femaleid
                    couple.CoupleIndex = next_couple_index()
                    add(couple)

                r = self.session.query(tar2Registration) \
                    .filter(tar2Registration.CategoryRef == entry.tarCategory.CategoryIndex) \
                    .filter(tar2Registration.CoupleRef == couple.CoupleIndex) \
                    .filter(tar2Registration.Number == number).first()
                if not r:
                    compositionName = self.session.query(srcRegistration_Title) \
                            .filter(srcRegistration_Title.number == number).first()
                    r = tar2Registration()
                    r.CoupleRef = couple.CoupleIndex
                    r.CategoryRef = entry.tarCategory.CategoryIndex
                    r.Number = number
                    r.CompositionName = compositionName.title if compositionName else ''
                    r.Registered = 1
                    r.RegTrainerRef = d.TrainerRef
                    r.RegChiefRef = d.ChiefRef
                    r.PaidEntry = 0.0
                    r.ProgramRefs = '.%s.' % reduce(lambda x, y: '%s.%s' % (x, y), programs)
                    add(r)

            progress.close()
            QMessageBox.information(self, u'Information', u'Информация успешно импортирована в счётную программу')
        except Exception, e:
            import traceback

            message = u'Ошибка импорта: ' + unicode(e) + '\n'
            message += traceback.format_exc()
            QMessageBox.information(self, u'Information', message)
            self.session.begin()
            self.session.commit()
            for item in items:
                try:
                    pass
                    #self.session.delete(item)
                except Exception, e:
                    print 'Error while deleting item %s: %s' % item, e
            progress.close()

